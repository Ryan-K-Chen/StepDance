#ifndef __FREQUENCY_MAP__
#define __FREQUENCY_MAP__

// ARRAY STARTS WITH C!

#define NOTE_C  0
#define NOTE_C_ 1
#define NOTE_D  2
#define NOTE_D_ 3
#define NOTE_E  4
#define NOTE_F  5
#define NOTE_F_ 6
#define NOTE_G  7
#define NOTE_G_ 8
#define NOTE_A  9
#define NOTE_A_ 10
#define NOTE_B  11
#define NOTE_B_ 12

float ZERO_FREQUENCIES [12] {
    16.35f,
    17.32f,
    18.35f,
    19.45f,
    20.60f,
    21.83f,
    23.12f,
    24.50f,
    25.96f,
    27.50f,
    29.14f,
    30.87f
};

float get_frequency(uint8_t note, uint8_t octave) {
    return ZERO_FREQUENCIES[note] * pow(2, octave);
}

#endif