
struct midi_note_t {
	float frequency;
	uint32_t start_time;
	uint32_t duration;
};

midi_note_t MIDI_FILE [] = {
    {440.0, 0, 10000},
};