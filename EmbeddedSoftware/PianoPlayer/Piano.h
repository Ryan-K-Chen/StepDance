#ifndef PIANO_H
#define PIANO_H

#include "StepperMotor.h"
#include "ClockTimer.h"
#include "A440.h"

struct two_pin_t {
    uint8_t pins[2];
    const uint8_t &operator[](uint8_t i) const {
        return pins[i];
    }
};

struct serial_input_t {
    float  vibrato;
    int8_t octave;
    serial_input_t() : vibrato(1.0), octave(4) { }
};


class Piano {
private:
    StepperMotor* steppers_;
    uint8_t num_steppers_;
    uint8_t s0_, s1_, s2_, muxin1_, muxin2_;
    uint16_t button_state_;
    ClockTimerf button_update_ct_;
    ClockTimerf serial_timer_;
    uint32_t prev_ser_write_;

public:
    serial_input_t serial_input;

    Piano() : 
        steppers_(NULL), 
        num_steppers_(0), 
        s0_(-1), s1_(-1), s2_(-1), 
        muxin1_(-1), muxin2_(-1),
        button_update_ct_(50), serial_timer_(10), prev_ser_write_(0) { }

    void make_steppers(two_pin_t* stepper_pins, uint8_t num_steppers){
        num_steppers_ = num_steppers;
        steppers_ = new StepperMotor[num_steppers];
        for(uint8_t i = 0; i < num_steppers; ++i) {
            steppers_[i].set_pins(stepper_pins[i][0], stepper_pins[i][1]);
            steppers_[i].begin();
        }
    }

    void make_button_mux(uint8_t* mux_pins){
        s0_ = mux_pins[0];
        s1_ = mux_pins[1];
        s2_ = mux_pins[2];
        muxin1_ = mux_pins[3];
        muxin2_ = mux_pins[4];
        pinMode(s0_, OUTPUT);
        pinMode(s1_, OUTPUT);
        pinMode(s2_, OUTPUT);
        pinMode(muxin1_, INPUT);
        pinMode(muxin2_, INPUT);
    }

    uint16_t get_button_state() {
        return button_state_;
    }

    void update() {
        uint32_t current_time = micros();
        uint16_t prev_button_state = button_state_;

        // && abs(micros() - prev_ser_write_) > 20000
        if(Serial.available() >= 5 ) {
            while(Serial.available() > 5) Serial.read();
            Serial.readBytes((uint8_t*) &(serial_input.vibrato), 4);
            Serial.readBytes((uint8_t*) &(serial_input.octave), 1);
            prev_ser_write_ = micros();
        }
            Serial.write(serial_input.octave);

        if(button_update_ct_.ready(current_time)){
            for(uint8_t i = 0; i < 8; ++i){
                digitalWrite(s0_, i & 0b001);
                digitalWrite(s1_, i & 0b010);
                digitalWrite(s2_, i & 0b100);
                uint8_t mux1 = digitalRead(muxin1_);//(analogRead(muxin1_) > 127);
                // uint8_t mux1 = (analogRead(muxin1_) > 127);
                // uint8_t mux2 = (analogRead(muxin2_) > 127);
                if (mux1) button_state_ |=  (1 << i);
                else      button_state_ &= ~(1 << i);
                if(i < 4){
                    uint8_t mux2 = digitalRead(muxin2_);//(analogRead(muxin2_) > 127);
                    if (mux2) button_state_ |=  (1 << (i + 8));
                    else      button_state_ &= ~(1 << (i + 8));
                }
            }
            // Serial.println(button_state_, BIN);
        }

        for(uint8_t i = 0; i < 12; ++i){
            bool old_set = (prev_button_state & (1 << i)) == 0; 
            bool new_set = (button_state_ & (1 << i)) == 0;
            
            if(old_set == 0 && new_set == 1){
                // SCHEDULE PRESS
                bool leave = false;
                for(uint8_t j = 0; j < num_steppers_ && !leave; ++j) {
                    if(!steppers_[j].press) {
                        steppers_[j].press = new Press(i,serial_input.octave);
                        // steppers_[j].set_frequency(steppers_[j].press->frequency);
                        // Serial.print("Scheduled press on note "); Serial.println(i);
                        leave = true;
                    } 
                }
            } else if (old_set == 1 && new_set == 0){
                // REMOVE PRESS
                bool leave = false;
                for(uint8_t j = 0; j < num_steppers_ && !leave; ++j) {
                    if(steppers_[j].press){
                        // Serial.println(steppers_[j].press->note); 
                        // Serial.println(i); 
                        if(steppers_[j].press->note == i) {
                            delete steppers_[j].press;
                            steppers_[j].press = NULL;
                            steppers_[j].set_frequency(0);
                            // Serial.print("Removed press on note "); Serial.println(i);
                            // leave = true;
                        } 
                    }
                }
            }
            // Serial.println("finished");
        }

        for(uint8_t i = 0; i < num_steppers_; ++i) {
            if(steppers_[i].press){
                steppers_[i].press->vibrato = serial_input.vibrato;
                steppers_[i].press->octave = serial_input.octave;
            }
            steppers_[i].update();
        }
    }
};

#endif
