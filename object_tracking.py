import cv2
import numpy as np
import imutils
import time
import mediapipe as mp
import serial
import pyttsx3
#https://www.youtube.com/watch?v=EgjwKM3KzGU&ab_channel=NicholasRenotte
vid = cv2.VideoCapture(0)
engine = pyttsx3.init()
mp_hands = mp.solutions.hands #https://google.github.io/mediapipe/solutions/hands.html
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) #video stream, lowkey looks at where hand was previously increase speed by decreasing complexity
mp_draw = mp.solutions.drawing_utils
port ='/dev/cu.usbmodem14201'  #14101 left  #14201 right (probably)
baud_rate = 115200
#arduino = serial.Serial(port, baud_rate)
tip_list = [8,12,16,20]
joint_list = [[7,6,5],[11,10,9],[15,14,13],[19,18,17]]
def finger_angles (hand_landmarks):
    angles = []
    for joint in joint_list:
        a = [hand_landmarks.landmark[joint[0]].x, hand_landmarks.landmark[joint[0]].y]
        b = [hand_landmarks.landmark[joint[1]].x, hand_landmarks.landmark[joint[1]].y]
        c = [hand_landmarks.landmark[joint[2]].x, hand_landmarks.landmark[joint[2]].y]
        radians = np.arctan2(c[1]-b[1], c[0] - b[0]) - np.arctan2(a[1]-b[1], a[0] - b[0])
        angle = np.abs(radians*180.0/np.pi)
        if angle > 180.0:
            angle = 360 - angle
        angles.append(angle)
    print(angles[0])
    if all(angle < 30 for angle in angles):
        print('CLOSED HAND')
last_7 = np.zeros((7,), dtype=int)
state = 0
while(True):  
    ret, frame = vid.read()
    frame = imutils.resize(frame, width=700)
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    h, w, c = frame.shape
    if results.multi_hand_landmarks: #[0], [1], if multiple hands
        fingers = []
        for hand_landmarks in results.multi_hand_landmarks: 
            for id in range (0,len(tip_list)):
                if hand_landmarks.landmark[tip_list[id]].y < hand_landmarks.landmark[tip_list[id]-2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)    
            if fingers[0] + fingers[2] + fingers[3] == 0 and fingers[1] ==1:
                print(':(')
            if 1 not in fingers[:2] and fingers[3] == 1:
                tstate = 0
                if np.all(last_7==tstate):
                    print('STOP')
                    state = 0
                last_7 = np.delete(last_7, 0)
                last_7 = np.append(last_7, tstate)
            elif fingers[1]==1 and fingers[2]==1 and fingers[0]+fingers[3]==0: 
                tstate = 1
                if np.all(last_7==tstate):
                    print('GO')
                    state = 1
                last_7 = np.delete(last_7, 0)
                last_7 = np.append(last_7, tstate)
            else:
                last_7 = np.delete(last_7, 0)
                last_7 = np.append(last_7, 3)
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x *w), int(lm.y*h)
                cv2.circle(frame, (cx,cy), 3, (255,0,255), cv2.FILLED)
                if id == 8: 
                    string='X{0:d}Y{1:d}S{2:d}'.format(cx,cy,state)
                    print(string)
                    #arduino.write(string.encode('utf-8'))
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)   
    cv2.imshow('frame', cv2.flip(frame, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 0xFF is just binary stuff
        break
vid.release()  # After the loop release the cap object
cv2.destroyAllWindows()  # Destroy all the windows




'''------------------------------NOTES------------------------------
- RGB order = BGR

'''      #print(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP])

'''     for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_area:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        if biggest is None or w*h>biggest_size:
            biggest = c
            biggest_size = w*h    
            print(x, y , w, h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            string='X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
            print(string)
            arduino.write(string.encode('utf-8'))
'''