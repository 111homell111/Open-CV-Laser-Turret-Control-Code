import cv2
import numpy as np
import imutils
import time
import serial
vid = cv2.VideoCapture(0)
min_area = 8000
motionCounter = 0
port ='/dev/cu.usbmodem14201'
baud_rate = 9600
first_frame = None
#arduino = serial.Serial(port, baud_rate)

while(True):  
    ret, frame = vid.read()
    frame = imutils.resize(frame, width=500)
    bilateral_filtered_image = cv2.bilateralFilter(frame, 7, 150, 150)
    gray = cv2.cvtColor(bilateral_filtered_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    state = 'Unoccupied'
    if first_frame is None:
        first_frame = gray
        continue
    frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(first_frame))   #  delta = |background_model – current_frame|
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    cnts = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts) 
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_area:

            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        state = "Occupied"
    #arduino.write...
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
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/