#ifndef PRESS_H
#define PRESS_H

class Press {
public:
    uint8_t note;
    float frequency;
    float vibrato;
    Press (uint8_t note_, float frequency_) : note(note_), frequency(frequency_) , vibrato(0.0){ }
};

#endif