import cv2
import imutils
import time
import numpy as np
import sklearn

print(sklearn.__version__)
past_time = 0
vid = cv2.VideoCapture(0)
last_3 = np.zeros((5,), dtype=int)
print("hello!!!!")

while(True):  
    ret, frame = vid.read()
    frame = imutils.resize(frame, width=700)
    current_time = time.time()
    fps = str(int(1/(current_time-past_time)))
    past_time = current_time
    frame = cv2.flip(frame, 1)

    last_3 = np.delete(last_3, 0)
    last_3 = np.append(last_3, int(fps))
    fps = int(np.average(last_3))


    cv2.putText(frame, "FPS: {}".format(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 0xFF is just binary stuff
        break
vid.release()  # After the loop release the cap object
cv2.destroyAllWindows()  # Destroy all the windows


'''
25-30 fps
'''