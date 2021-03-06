from numpy import byte
import pretty_midi
import sys
import struct
import serial

def get_start_time(note_arr_ele):
    return note_arr_ele[1]

# Set up communication on serial port
# Open COM port (the COM port must be chosen manually)
try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=3)
    # ser = serial.Serial('COM15', 115200, timeout=3)
except Exception as e:
    print(e)
    ser = None
    print('\033[93m' + "Unable to open the serial port, try a different COM port" + '\033[0m')

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
        # if (sys.argv[2] == "notes"):
        #     note_arr.append((piano_key, start_time, duration))
        # elif (sys.argv[2] == "serial"):
        #     note_arr.append(struct.pack('fII', freq, start_time, duration))  # Might need to be >fII
        # else:
        note_arr.append((freq, start_time, duration, piano_key))

        # print(f'{freq:10} {start_time:10} {duration:10}'

note_arr.sort(key=get_start_time)
if (sys.argv[2] == "serial"):
    # send to serial out
    print(note_arr)
    for ele in note_arr:
        # each ele consists of (frequency, start_time, duration) in byte format (float, uint32, uint32)
        # print(ele)
        byte_form = struct.pack('<fII', ele[0], ele[1], ele[2])
        if ser is not None:
            while ser.in_waiting == 0:
                pass
                # sleep(0.02)
                # print("Waiting on data from Teensy")
            answer = int.from_bytes(ser.read(1), "little")
            # print("%x" % answer)
            # if answer == 1:
            # print("%x, %x, %x, %x, %x, %x, %x, %x, %x, %x, %x, %x, " % (ele[0], ele[1], ele[2], ele[3], ele[4], ele[5], ele[6], ele[7], ele[8], ele[9], ele[10], ele[11]))
            print(answer)
            print(byte_form)
            # print(len(byte_form))
            ser.write(byte_form)
    
    while True:
        pass

elif (sys.argv[2] == "notes"):
    for ele in note_arr:
        print("%s" % (ele[3]))
        print("%d" % (ele[1]))
        print("%s" % (ele[2]))
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

ser.close()
