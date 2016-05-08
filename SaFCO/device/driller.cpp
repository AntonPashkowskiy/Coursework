#include "driller.h"

bool Driller::digitalRead_approx(uint8_t pinNumber) {
  uint8_t true_times = 0;
  for (int i = 0; i < 5; i++) {
    true_times += digitalRead(pinNumber);
  }
  if (true_times == 5) {
    return true;
  }
  return false;
}

void Driller::setZeroPhase() {
  for (int k = PHASE1_PIN; k <= PHASE4_PIN; k++) {
    digitalWrite(k, LOW);
  }
}

void Driller::setAxis(uint8_t axis) {
  if (axis <= Z) {
    this->setZeroPhase();
    digitalWrite(CHANNEL_X_PIN, axis == X);
    digitalWrite(CHANNEL_Y_PIN, axis == Y);
    digitalWrite(CHANNEL_Z_PIN, axis == Z);
  }
}

void Driller::setDrillingState(bool state) {
  analogWrite(DRILL_PIN, DRILL_POWER * state);
}

void Driller::returnZToStart(bool mayBeInHole) {
  this->setDrillingState(mayBeInHole);
  while (this->moveOneStep(Z, true));
  this->setDrillingState(false);
  this->_coords[Z] = 0;
}

void Driller::returnToStart(uint8_t axis) {
  returnZToStart();
  if (axis != Z) {
    while (moveOneStep(axis, false));
    this->_coords[axis] = 0;
  }
}

bool Driller::checkPower() {
  if (analogRead(POWER_PIN) < 400) {
    return false;
  }
  return true;
}

bool Driller::checkIfMovementAllowed(uint8_t axis, bool direction) {
  if (!this->checkPower()) {
    return false;
  }
  this->setAxis(axis);
  if (axis == Z) {
    if (direction) {
      return !digitalRead_approx(AXIS_Z_START_PIN);
    } else {
      return !digitalRead_approx(AXIS_END_PIN);
    }
  } else {
    if (direction) {
      return !digitalRead_approx(AXIS_END_PIN);
    } else {
      return !digitalRead_approx(AXIS_XY_START_PIN);
    }
  }
}

bool Driller::moveOneStep(uint8_t axis, bool direction, long delayDuration) {
  if (checkIfMovementAllowed(axis, direction)) {
    _phase[axis] += direction ? MOVE_F : MOVE_B;
    _phase[axis] %= 4;
    this->setAxis(axis);
    digitalWrite(PHASE1_PIN + _phase[axis], HIGH);
    delay(delayDuration ? delayDuration : _delayDurations[axis]);
    this->_coords[axis] += -1 + 2 * direction;
  } else {
    this->setZeroPhase();
    return false;
  }
  this->setZeroPhase();
  return true;
}

bool Driller::relativeMoveTo(uint8_t axis, int16_t stepsNumber) {
  bool direction;
  if (stepsNumber >= 0) {
    direction = true;
  } else {
    direction = false;
    stepsNumber *= -1;
  }
  for (; stepsNumber > 0; stepsNumber--) {
    if (!moveOneStep(axis, direction)) {
      return false;
    }
  }
  return true;
}

bool Driller::moveTo(int16_t x, int16_t y) {
  if (x < 0 || y < 0 || x > X_MAX || y > Y_MAX) {
    return false;
  }
  bool xRes = relativeMoveTo(X, x - this->_coords[X]) || x == 0;
  bool yRes = relativeMoveTo(Y, y - this->_coords[Y]) || y == 0;
  this->_coords[X] = this->_coords[X] * (!(x == 0));
  this->_coords[Y] = this->_coords[Y] * (!(y == 0));
  return xRes && yRes;
}

bool Driller::touchCircuit() {
  while (moveOneStep(Z, false) && digitalRead_approx(DRILL_TOUCH_PIN));
  if (digitalRead_approx(DRILL_TOUCH_PIN)) {
    this->returnZToStart();
    return false;
  }
  return true;
}

bool Driller::makeHole() {
  if (!touchCircuit()) {
    return false;
  }
  for (int i = 0; i < 600; i++) {
    moveOneStep(Z, false);
  }

  this->setDrillingState(true);
  while (moveOneStep(Z, false, 20) && !digitalRead_approx(DRILL_TOUCH_PIN));
  while (!digitalRead_approx(DRILL_TOUCH_PIN));

  this->returnZToStart();
  return true;
}

Driller::Driller() {
  pinMode(PHASE1_PIN, OUTPUT);
  pinMode(PHASE2_PIN, OUTPUT);
  pinMode(PHASE3_PIN, OUTPUT);
  pinMode(PHASE4_PIN, OUTPUT);
  pinMode(CHANNEL_X_PIN, OUTPUT);
  pinMode(CHANNEL_Y_PIN, OUTPUT);
  pinMode(CHANNEL_Z_PIN, OUTPUT);
  pinMode(AXIS_Z_START_PIN, INPUT);
  pinMode(AXIS_XY_START_PIN, INPUT);
  pinMode(AXIS_END_PIN, INPUT);
  pinMode(POWER_PIN, INPUT);
  pinMode(DRILL_PIN, OUTPUT);
}

bool Driller::Init() {
  if (!this->checkPower()) {
    return false;
  }
  this->returnToStart(X);
  this->returnToStart(Y);
  this->_initialised = true;
  return true;
}

bool Driller::IsInitialised() {
  return _initialised;
}

bool Driller::CheckPower() {
  return this->checkPower();
}

bool Driller::DrillAt(int16_t x, int16_t y) {
  if (!this->moveTo(x, y) || !this->makeHole()) {
    return false;
  }
  return true;
}

bool Driller::MoveTo(int16_t x, int16_t y) {
  return this->moveTo(x, y);
}

bool Driller::TouchCircuit() {
  if (touchCircuit()) {
    this->returnZToStart(false);
    return true;
  }
  return false;
}

int16_t* Driller::GetCoords() {
  int16_t *coords = new int16_t[2];
  coords[0] = _coords[X];
  coords[1] = _coords[Y];
  return coords;
}
