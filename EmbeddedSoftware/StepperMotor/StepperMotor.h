#ifndef STEPPERMOTOR_H
#define STEPPERMOTOR_H

#include "Note.h"
#include "Press.h"
#include "A440.h"
#include "ClockTimer.h"

class StepperMotor {
private:
    uint8_t pin_, en_;
    bool enabled_;
    ClockTimerf ct;

public:
    Note* note;
    Press* press;

    StepperMotor() : pin_(-1), en_(-1), enabled_(0), ct(1), note(NULL), press(NULL) {}
    StepperMotor(uint8_t pin, uint8_t en) : pin_(pin), en_(en), enabled_(0), ct(1), note(NULL), press(NULL) {}

    void set_pins(uint8_t pin, uint8_t en){
        pin_ = pin;
        en_ = en;
    }

    void begin() {
        pinMode(pin_, OUTPUT);
        pinMode(en_, OUTPUT);
    }

    void step() {
        digitalWrite(pin_, HIGH);
        digitalWrite(pin_, LOW);
        digitalWrite(en_, HIGH);
    }

    void set_frequency(float frequency) {
        if (frequency > 0) {
            ct.set_frequency(frequency);
            enabled_ = 1;
        }
        else {
            enabled_ = 0;
        }
    }

    void update() {
        if (press) {
            // set_frequency(press->frequency);
            set_frequency(get_frequency(press->note, press->octave) * press->vibrato);
        }
        // if (!enabled_) {
        //     digitalWrite(en_, LOW);
        // } else 
        if (ct.ready(micros()) && enabled_) {
            step();
        }
    }
};

#endif