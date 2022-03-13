#include "StepperScheduler.h"

#define REQUEST_NOTE 0x1

#define NUM_STEPPERS 5
const two_pin_t pins[NUM_STEPPERS] = {
  {2,3},
  {4,5},
  {6,7},
  {8,9},
  {10,11}
};

StepperScheduler scheduler;

ClockTimerf ledt(2);
bool leds = 0;

void setup() {
  Serial.begin(115200);
  scheduler.make_steppers(pins, NUM_STEPPERS);

  pinMode(13, OUTPUT);

  delay(2000);
  while(Serial.available()) {
    Serial.read();
  }
  Serial.write(REQUEST_NOTE);
}

void loop() {
  static const uint32_t midi_start_time = micros();
  static Note midi_note(0.0,0,0);

  if (Serial.available() == 12) {
    Serial.readBytes((uint8_t*) &(midi_note.frequency), 4);
    Serial.readBytes((uint8_t*) &(midi_note.start), 4);
    Serial.readBytes((uint8_t*) &(midi_note.duration), 4);
  }
  
  uint32_t current_time = micros();

  if(midi_note.frequency != 0.0){
    int32_t diff = (current_time - midi_start_time) - midi_note.start;
    if (diff >= 0) {
      midi_note.start = current_time;
      midi_note.duration -= diff;
      scheduler.schedule_note(midi_note);
//      if(!scheduler.schedule_note(midi_note)) {
        midi_note.frequency = 0.0;
        Serial.write(REQUEST_NOTE);
//      }
    }
  }

  if(ledt.ready(current_time)) {
    leds = !leds;
    digitalWrite(13, leds);
  }
  
  scheduler.update();
}
