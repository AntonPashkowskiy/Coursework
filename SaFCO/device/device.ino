#include <stdint.h>
#include <stdbool.h>
#include "driller.h"

Driller *driller = NULL;

void setup() {
  Serial.begin(230400);
  while (!Serial);
  driller = new Driller();
}

void loop() {

}

void readAllDataFromSerial() {
  Serial.readStringUntil('\n');
  while (Serial.available() > 0) {
    Serial.read();
    delay(20);
  }
}

void serialEvent() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil(':');

    // power independent commands
    if (command == "connect") {
      readAllDataFromSerial();
      Serial.print("res: ");
      Serial.println(true);
      if (driller->Init()) {
        Serial.print("ready: ");
        Serial.println(true);
      } else {
        Serial.println("error: 1");
      }
      return;
    }

    if (!driller->IsInitialised()) {
      return;
    }

    if (command == "coords") {
      readAllDataFromSerial();
      int16_t *coords = driller->GetCoords();
      Serial.print("res: ");
      Serial.print(coords[0]);
      Serial.print(' ');
      Serial.println(coords[1]);
      delete[] coords;
      return;
    }

    if (!driller->CheckPower()) {
      readAllDataFromSerial();
      Serial.println("error: 1");
      return;
    }

    // power dependent commands
    if (command == "move") {
      pinMode(13, OUTPUT);
      digitalWrite(13, HIGH);
      long x = Serial.parseInt();
      long y = Serial.parseInt();
      readAllDataFromSerial();
      bool res = driller->MoveTo(x, y);
      Serial.print("res: ");
      Serial.println(res);
      digitalWrite(13, LOW);
    } else if (command == "drill") {
      long x = Serial.parseInt();
      long y = Serial.parseInt();
      Serial.readStringUntil('\n');
      bool res = driller->DrillAt(x, y);
      Serial.print("res: ");
      Serial.println(res);
    } else if (command == "touch") {
      Serial.readStringUntil('\n');
      bool res = driller->TouchCircuit();
      Serial.print("res: ");
      Serial.println(res);
    } else {
      Serial.println("error: 0");
      Serial.readStringUntil('\n');
    }
  }
}
