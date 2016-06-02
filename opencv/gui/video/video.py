"""
Read, display, save video
Capture from camera and display video
cv2.
    VideoCapture()
    VideoWriter()
"""

# need VideoCapture object; argument is either device index or name of video file
# device index -- specifies which camera; normally one camera, so pass 0 or -1
# in the end, RELEASE the capture!

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while(True):
    # capture frame-by-frame
    ret, frame = cap.read() # returns a bool (frame read correctly=True); use to find video end
    # cap may not have initialized capture; check with cap.isOpened()
    #   True -- OK otherwise open using cap.open()
    # access video features using cap/get(propId), propId number from 0 to 18
    #   denotes property of video; see Property Identifier
    # modify properties using cap.set(propId, value)
    #   ex. frame width and height with cap.get(3) and cap.get(4)
    # if 640x480 default but want 320x240, use ret = cap.set(propId, value)
    #   ex. ret = cap.set(3,320) and ret = cap.set(4, 240)

    # our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# when everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
