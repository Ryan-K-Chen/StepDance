import pretty_midi
import sys
import struct

def get_start_time(note_arr_ele):
    return note_arr_ele[1]

note_arr = []

midi_data = pretty_midi.PrettyMIDI("../midiFiles/" + sys.argv[1] + ".mid")
print("duration:",midi_data.get_end_time())
print(f'{"note":>10} {"start":>10} {"duration":>10}')
for instrument in midi_data.instruments:
    print("instrument:", instrument.program);
    for note in instrument.notes:
        freq = round(pretty_midi.note_number_to_hz(note.pitch), 2)
        start_time = int(note.start * 1000)
        duration = int(note.end * 1000) - start_time

        note_arr.append((freq, start_time, duration))

        # print(f'{freq:10} {start_time:10} {duration:10}'

note_arr.sort(key=get_start_time)

f = open("../midiFiles/midiBins/" + str(sys.argv[1]) + ".bin", "wb")

for ele in note_arr:
    f.write(struct.pack('>fII', ele[0], ele[1], ele[2]))

print(note_arr)
f.close()
