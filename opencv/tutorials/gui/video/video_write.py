"""
write to a video file
create VideoWriter object
    -specify output video file name
    -specify FourCC code
    -# of frames per second
    -isColor flag (True -- encoder expects color frame, otw grayscale)
FourCC is 4-byte code specifying video codec (platform dependent)
    Fedora: DIVX, XVID, MJPG, X264, WMV1, WMV2
    Windows: DIVX
"""

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame, 0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# release everything if job is finished
out.release();
cap.release()
# out.release()
cv2.destroyAllWindows()
