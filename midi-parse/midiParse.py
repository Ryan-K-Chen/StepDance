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
        piano_key = pretty_midi.note_number_to_name(note.pitch)
        freq = round(pretty_midi.note_number_to_hz(note.pitch), 2)
        start_time = int(note.start * 1000000)
        duration = int(note.end * 1000000) - start_time
        if (sys.argv[2] == "notes"):
            note_arr.append((piano_key, start_time, duration))
        elif (sys.argv[2] == "serial"):
            note_arr.append(struct.pack('>fII', freq, start_time, duration))
        else:
            note_arr.append((freq, start_time, duration))

        # print(f'{freq:10} {start_time:10} {duration:10}'

note_arr.sort(key=get_start_time)
if (sys.argv[2] == "serial"):
    # send to serial out
    for ele in note_arr:
        # each ele consists of (frequency, start_time, duration) in byte format (float, uint32, uint32)
        print(ele)
elif (sys.argv[2] == "notes"):
    for ele in note_arr:
        print("%s" % (ele[0]))
elif (sys.argv[2] == "header"):
    f = open("../midiFiles/midiHeaders/" + str(sys.argv[1]) + ".h", "w")
    f.write("struct midi_note_t {\n\tfloat frequency;\n\tuint32_t start_time;\n\tuint32_t duration;\n};\n\nmidi_note_t MIDI_FILE [] = {\n")

    for ele in note_arr:
        f.write("\t{%.2f, %d, %d},\n" % (ele[0], ele[1], ele[2]))
    f.write("};")

    f.close()
    print("written to " + str(sys.argv[1]) + ".h")
elif (sys.arv[2] == "bin"):
    f = open("../midiFiles/midiBins/" + str(sys.argv[1]) + ".bin", "wb")

    for ele in note_arr:
        f.write(struct.pack('>fII', ele[0], ele[1], ele[2]))

    f.close()
    print("written to " + str(sys.argv[1]) + ".h")
