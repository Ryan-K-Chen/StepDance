#include "Piano.h"

#define NUM_STEPPERS 5
const two_pin_t pins[NUM_STEPPERS] = {
  {2,3},
  {4,5},
  {6,7},
  {8,9},
  {10,11}
};

uint8_t mux_pins[5] = { A0, A1, A2, 12, A3 }; //A6, A7 };

Piano piano;

void setup() {
  Serial.begin(115200);
  piano.make_steppers(pins, NUM_STEPPERS);
  piano.make_button_mux(mux_pins);
  while(Serial.available()) {
    Serial.read();
  }
}

void loop() {
  piano.update();
}
