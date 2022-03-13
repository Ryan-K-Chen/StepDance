#ifndef PRESS_H
#define PRESS_H

class Press {
public:
    uint8_t note;
    uint8_t octave;
    float vibrato;
    Press (uint8_t note_, uint8_t octave_) : note(note_), octave(octave_), vibrato(1.0){ }
};

#endif