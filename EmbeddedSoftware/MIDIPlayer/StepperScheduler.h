#ifndef STEPPERSCHEDULER_H
#define STEPPERSCHEDULER_H

#include "StepperMotor.h"
#include "Note.h"

struct two_pin_t {
  uint8_t pins[2];
  const uint8_t& operator[] (uint8_t i) const {
    return pins[i];
  }
};

class StepperScheduler {
private:
    StepperMotor* steppers_;
    uint8_t num_steppers_;
public:
    StepperScheduler() : steppers_(NULL), num_steppers_(0) {}

    void make_steppers(two_pin_t* stepper_pins, uint8_t num_steppers){
        num_steppers_ = num_steppers;
        steppers_ = new StepperMotor[num_steppers];
        for(uint8_t i = 0; i < num_steppers; ++i) {
            steppers_[i].set_pins(stepper_pins[i][0], stepper_pins[i][1]);
            steppers_[i].begin();
        }
    }

    uint8_t schedule_note(Note note){
        for(uint8_t i = 0; i < num_steppers_; ++i) {
            if(!steppers_[i].note) {
                steppers_[i].note = new Note(note);
                steppers_[i].set_frequency(note.frequency);
                return 1;
            } 
        }
        return 0;
    }

    void update() {
        uint32_t current_time = micros();

        for(uint8_t i = 0; i < num_steppers_; ++i) {
            if(steppers_[i].note){
                if(abs(current_time - steppers_[i].note->start) >= steppers_[i].note->duration) {
                    delete steppers_[i].note;
                    steppers_[i].note = NULL;
                    steppers_[i].set_frequency(0);
                }
            }
            steppers_[i].update();
        }
    }
};

#endif
