#ifndef NOTE_H
#define NOTE_H

class Note {
public:
    float frequency;
    uint32_t start;
    uint32_t duration;
    Note(float frequency_, uint32_t start_, uint32_t duration_) : 
        frequency(frequency_),
        start(start_),
        duration(duration_) {}
};

#endif
