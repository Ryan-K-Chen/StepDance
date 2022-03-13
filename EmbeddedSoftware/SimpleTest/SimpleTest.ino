#include "StepperMotor.h"
#include "Note.h"

StepperMotor sm(2,3);
StepperMotor sm2(4,5);

ClockTimerf notetimer(2);

void setup() {
  sm.begin();
  sm2.begin();
  sm.set_frequency(440);
  sm2.set_frequency(103.83 * 8);
}

void loop() {
  static uint8_t note = 5;
  static float mult = 1.0;
  static float notes[] = {55.0, 58.27, 61.74, 65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83};
  static float freq = 55.0;
//  if(notetimer.ready(micros())){
//    if((++note) > 11){
//      note = 0;
//      mult *= 2;
//      if(mult >= 500){
//        mult = 1.0;
//      }
//    }
//    sm.set_frequency(notes[note] * mult);
//    Serial.print("New Note: "); Serial.println(notes[note] * mult);
//  }
  sm.update();
  sm2.update();
}
