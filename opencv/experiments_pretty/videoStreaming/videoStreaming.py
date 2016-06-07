import numpy as np
import cv2
from onlinevid import OnlineVideo
import time

url = 'http://192.168.0.108:8080/video'

cap = OnlineVideo(url)

while(True):
    frame = cap.getFrame()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
    elif cv2.waitKey(1) & 0xFF == ord('r'):
        cap = OnlineVideo(url)
        print('retarting')
cap.killStream()
cv2.destroyAllWindows()
