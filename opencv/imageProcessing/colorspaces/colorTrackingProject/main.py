import numpy as np
import cv2
import util

vidHandle = cv2.VideoCapture(0)
while(True):
    ret, frame = vidHandle.read()
    frW, frL, ch = np.shape(frame)
    frL = int(frL)
    frW = int(frW)
    util.drawXHair(frame, frW/2, frL/2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vidHandle.release()
cv2.destroyAllWindows()
