import cv2
import mediapipe as mp
import time
import math

def y_to_vib(ypos, baseline):
    vib_multiplier = 0.2
    diff = 1 - (ypos - baseline) * vib_multiplier
    return round(diff, 2)

def is_fist(index, thumb, prev_pos):
    distance = math.sqrt((index.x - thumb.x)**2 + (index.y - thumb.y)**2 + (index.z - thumb.z)**2)
    if (prev_pos):
        # was pinched before so require more distance to uninitialize
        if (distance > 0.15):
            # print("pinched!")
            return False
        else:
            return True
    else:
        if (distance < 0.06):
            # print("pinched!")
            return True
        else:
            return False
        # print(distance)
        # return distance

def left_or_right(thumb, pinky):
    # print("thumb x: %.2f" % (thumb.x))
    # print("pinky x: %.2f" % (pinky.x))
    result = 0
    if (pinky.x > thumb.x):
        print("left")
        result = -1
    else:
        print("right")
        result = 1
    return result

def left_or_right_conf(thumb, pinky, conf):
    # print("thumb x: %.2f" % (thumb.x))
    # print("pinky x: %.2f" % (pinky.x))
    result = 0
    if (conf >= 4):
        if (pinky.x > thumb.x):
            print("left")
            result = -1
        else:
            print("right")
            result = 1
        conf = 0
    else:
        conf += 1
    return (result, conf)


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.2,
                      min_tracking_confidence=0.2)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

handDetected = True
test = True
direction_conf = 0
starting_ypos = -1
was_pinched = False

while True:
    success, img = cap.read()
    if (test):
        test = False
        print("height: %d" % (img.shape[0]))
        print("width:  %d" % (img.shape[1]))

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        prev_y_pos = 0
        if (handDetected == False):
            # print("Hand Detected")
            # mostly for debuggin right now when need absolute confidence
            # direction, new_conf = left_or_right(results.multi_hand_landmarks[0].landmark[4], results.multi_hand_landmarks[0].landmark[8], direction_conf)
            # direction_conf = new_conf
            left_or_right(results.multi_hand_landmarks[0].landmark[4], results.multi_hand_landmarks[0].landmark[8])
            handDetected = True
        for handLms in results.multi_hand_landmarks:
            is_pinched = is_fist(handLms.landmark[8], handLms.landmark[4], was_pinched)
            if (not was_pinched and is_pinched):
                starting_ypos = handLms.landmark[4].y
                was_pinched = True
                print("y start: %.2f" % (starting_ypos))


            if (is_pinched):
                print("vib scale: %.2f" % (y_to_vib(handLms.landmark[4].y, starting_ypos)))
            else:
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

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    line_pos = starting_ypos * 720
    cv2.putText(img,"mid:_____________________________", (10,int(line_pos)), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    # cv2.putText(img,"top:_____________________________", (10,10), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    # cv2.putText(img,"bot:_____________________________", (10,720), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
