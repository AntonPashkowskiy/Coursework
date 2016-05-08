#ifndef H_DRILLER
#define H_DRILLER

#include <Arduino.h>

#define AXIS_Z_START_PIN A2
#define AXIS_XY_START_PIN A3
#define DRILL_TOUCH_PIN A3
#define AXIS_END_PIN A4
#define CHANNEL_X_PIN 9
#define CHANNEL_Y_PIN 7
#define CHANNEL_Z_PIN 6
#define PHASE1_PIN 2
#define PHASE2_PIN 3
#define PHASE3_PIN 4
#define PHASE4_PIN 5
#define DRILL_PIN 10
#define POWER_PIN A5

#define MOVE_F 1
#define MOVE_B 3
#define X 0
#define Y 1
#define Z 2
#define DRILL_POWER 80
#define X_MAX 10000
#define Y_MAX 5300

class Driller {
    bool _initialised = false;
    int16_t _coords[3];
    uint8_t _phase[3] = {0};
    long _delayDurations[3] = {10, 5, 3};
    bool digitalRead_approx(uint8_t pinNumber);
    void setZeroPhase();
    void setAxis(uint8_t axis);
    void setDrillingState(bool state);
    void returnZToStart(bool mayBeInHole = true);
    void returnToStart(uint8_t axis);
    bool checkPower();
    bool checkIfMovementAllowed(uint8_t axis, bool direction);
    bool moveOneStep(uint8_t axis, bool direction, long delayDuration = 0);
    bool relativeMoveTo(uint8_t axis, int16_t stepsNumber);
    bool moveTo(int16_t x, int16_t y);
    bool touchCircuit();
    bool makeHole();
  public:
    Driller();
    bool Init();
    bool IsInitialised();
    bool CheckPower();
    bool DrillAt(int16_t x, int16_t y);
    bool MoveTo(int16_t x, int16_t y);
    bool TouchCircuit();
    int16_t* GetCoords();
};

#endif  //H_DRILLER
