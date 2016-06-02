"""
Read, display video from a file
"""

import numpy as np
import cv2

cap = cv2.VideoCapture('vtest.avi')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # display the resulting frame
    cv2.imshow('frame', gray)
    # while displaying frame, use appropriate time for waitKey
    #   too little --> video very fast
    #   too high --> video too slow
    #   25 sec OK in normal cases
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# when everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
# NOTE: make sure proper versions of ffmpeg or gstreamer installed
