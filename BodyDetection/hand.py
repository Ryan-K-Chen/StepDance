import cv2
import mediapipe as mp
import time
import math
import serial
import struct

# scaling of window in %
window_scale = 20

# maximum and minimum vibrato values allowed for cases when tracking loses hand
vib_limit_high = 1.25
vib_limit_low = 0.75

# converts y position on screen to vibrato scale
# adjust multiplier to change vibrato intensity
def y_to_vib(ypos, baseline):
    vib_multiplier = 0.5
    diff = 1 - (ypos - baseline) * vib_multiplier
    return left_right_hand_result * diff

# detects whether the hand is currently pinching
def is_pinch(index, thumb, prev_pos):
    distance = math.sqrt((index.x - thumb.x)**2 + (index.y - thumb.y)**2 + (index.z - thumb.z)**2)
    if (prev_pos):
        # was pinched before so require more distance to unpinch
        if (distance > 0.15):
            return False
        else:
            return True
    else:
        if (distance < 0.06):
            return True
        else:
            return False

# returns whether hand is left or right when it first comes on screen
def left_or_right(thumb, pinky):
    # print("thumb x: %.2f" % (thumb.x))
    # print("pinky x: %.2f" % (pinky.x))
    result = 0
    if (pinky.x > thumb.x):
        result = 1
    else:
        result = -1
    return result

# returns whether hand is left or right, but requires several samples first
def left_or_right_conf(thumb, pinky, conf):
    # print("thumb x: %.2f" % (thumb.x))
    # print("pinky x: %.2f" % (pinky.x))
    sample_count = 4
    result = 0
    if (conf >= sample_count):
        if (pinky.x > thumb.x):
            result = 1
        else:
            result = -1
        conf = 0
    else:
        conf += 1
    return (result, conf)

# finds whether head is tilted
def detect_sloped(x_top, y_top, x_bottom, y_bottom):
    slope = (x_top - x_bottom) / (y_top - y_bottom)
    return slope

# function to handle serial output
def serial_output(vib_val, head_tilt_val):
    print("serial_vib  : %.2f" % serial_vib)
    print("serial_slope: %d" % serial_slope)

    if ser is not None or True:
        # Basically, we need to convert python data types to an array of bytes. We can do this by packing into a C
        # struct and then converting to a bytearray

        data_to_send = bytearray(struct.pack("fb", serial_vib, serial_slope))
        #ser.write(data_to_send)


cap = cv2.VideoCapture(0)

def make_1080p():
    cap.set(3, 1920)
    cap.set(4, 1080)

def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)

def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# uncomment whatever resolution your camera supports
# change_res()
# make_1080p()
# make_720p()
# make_480p()

# for hand detection
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.2,
                      min_tracking_confidence=0.2)
mpDraw = mp.solutions.drawing_utils

# for face mesh
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 1)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

pTime = 0
cTime = 0

handDetected = True
direction_conf = 0
starting_ypos = -1
was_pinched = False

height = 0
width = 0

# negative when left
# positive when right
left_right_hand_result = 0;

serial_slope = 0;
serial_vib = 0;

# Set up communication on serial port
# Open COM port (the COM port must be chosen manually)
try:
    ser = serial.Serial('COM15', 115200, timeout=3)
except Exception as e:
    print(e)
    ser = None
    print('\033[93m' + "Unable to open the serial port, try a different COM port" + '\033[0m')

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    height, width, _ = img.shape

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB.flags.writeable = False

    hand_results = hands.process(imgRGB)

    if hand_results.multi_hand_landmarks:
        prev_y_pos = 0
        if (handDetected == False):
            # print("Hand Detected")
            # mostly for debuggin right now when need absolute confidence
            # direction, new_conf = left_or_right(hand_results.multi_hand_landmarks[0].landmark[4], hand_results.multi_hand_landmarks[0].landmark[8], direction_conf)
            # direction_conf = new_conf
            left_right_hand_result = left_or_right(hand_results.multi_hand_landmarks[0].landmark[4], hand_results.multi_hand_landmarks[0].landmark[8])
            # if (left_right_hand_result > 0):
            #     print("right hand")
            # elif (left_right_hand_result < 0):
            #     print("left hand")

            handDetected = True
        for handLms in hand_results.multi_hand_landmarks:
            is_pinched = is_pinch(handLms.landmark[8], handLms.landmark[4], was_pinched)
            if (not was_pinched and is_pinched):
                starting_ypos = handLms.landmark[4].y
                was_pinched = True
                # print("y start: %.2f" % (starting_ypos))

            curr_vib_value = y_to_vib(handLms.landmark[4].y, starting_ypos)
            if (abs(curr_vib_value) > vib_limit_high or abs(curr_vib_value) < vib_limit_low):
                curr_vib_value = 0

            if (is_pinched):
                serial_vib = curr_vib_value
                # print("vib scale: %.2f" % (curr_vib_value))
            else:
                serial_vib = 0
                was_pinched = False
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                if (is_pinched and (id == 4 or id == 8)):
                    cv2.circle(img, (cx,cy), 15, (66, 245, 84), cv2.FILLED)
                else:
                    cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    else:
        handDetected = False
        starting_ypos = -1
        left_right_hand_result = 0

    # for face mesh creation
    face_results = faceMesh.process(imgRGB)
    if face_results.multi_face_landmarks:
        # for facial_landmarks in face_results.multi_face_landmarks:
        pt_top = face_results.multi_face_landmarks[0].landmark[10]
        x_top = int(pt_top.x * width)
        y_top = int(pt_top.y * height)

        pt_bottom = face_results.multi_face_landmarks[0].landmark[152]
        x_bottom = int(pt_bottom.x * width)
        y_bottom = int(pt_bottom.y * height)

        color = (100,100,0)
        slope_text = "straight"

        slope = -1 * detect_sloped(x_top, y_top, x_bottom, y_bottom)

        if (slope > 0.3):
            serial_slope = 1
            # print("head tilted right")
            color = (59, 255, 111)
            slope_text = "right"
        elif (slope < -0.3):
            serial_slope = -1
            # print("head tilted left")
            color = (255, 59, 59)
            slope_text = "left"
        else:
            serial_slope = 0

        cv2.circle(img, (x_top,y_top), 10, color, -1)
        cv2.circle(img, (x_bottom,y_bottom), 10, color, -1)
        cv2.line(img, (x_top,y_top), (x_bottom,y_bottom), color, 5)
        cv2.putText(img, slope_text, (x_top - 100,y_top), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)


    # write to serial out
    serial_output(serial_vib, serial_slope)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    line_pos = starting_ypos * height
    cv2.putText(img, str(round(serial_vib, 2)) + ":_____________________________", (10,int(line_pos)), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    # cv2.putText(img,"top:_____________________________", (10,10), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    # cv2.putText(img,"bot:_____________________________", (10,720), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    scaled_frame = rescale_frame(img, percent=window_scale)
    cv2.imshow('Step Dance', scaled_frame)
    # comment out scales you dont want
    # default
    # cv2.imshow("Image", img)

    # custom scales
    # frame150 = rescale_frame(img, percent=150)
    # cv2.imshow('frame150', frame150)
    # frame20 = rescale_frame(img, percent=20)
    # cv2.imshow('frame20', frame20)
    # frame200 = rescale_frame(img, percent=200)
    # cv2.imshow('frame200', frame200)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
