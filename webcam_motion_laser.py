import cv2
import numpy as np
import imutils
import time
import serial
vid = cv2.VideoCapture(0)
min_area = 8000
avg = None
motionCounter = 0
port ='/dev/cu.usbmodem14101'
baud_rate = 9600
#arduino = serial.Serial(port, baud_rate)
while(True):  
    biggest = None
    ret, frame = vid.read()
    frame = imutils.resize(frame, width=500)
    bilateral_filtered_image = cv2.bilateralFilter(frame, 7, 150, 150)
    gray = cv2.cvtColor(bilateral_filtered_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    state = 'Unoccupied'
    if avg is None:
        avg = gray.copy().astype('float')
    cv2.accumulateWeighted(gray, avg, 0.5)
    frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))   #  delta = |background_model – current_frame|
    thresh = cv2.threshold(frame_delta, 5, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=4)
    cnts = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)  # center of contour?
    for c in cnts:         # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_area:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        if biggest is None or w*h>biggest_size:
            biggest = c
            biggest_size = w*h    
            print(x, y , w, h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)
            state = "Occupied"
    #arduino.write
    cv2.putText(frame, "Room Status: {}".format(state), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, 'hi',(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow('frame', cv2.flip(frame, 1))
    cv2.imshow('thresh', cv2.flip(thresh, 1))
    cv2.imshow('frame delta', cv2.flip(frame_delta, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 0xFF is just binary stuff
        break
vid.release()  # After the loop release the cap object
cv2.destroyAllWindows()  # Destroy all the windows






'''------------------------------NOTES------------------------------
- RGB order = BGR

'''
