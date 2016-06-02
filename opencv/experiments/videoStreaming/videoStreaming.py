import numpy as np
import cv2
from onlinevid import OnlineVideo
import time

url = 'http://192.168.0.108:8080/video'
# cap = OnlineVideo('http://174.51.161.11/mjpg/1/video.mjpg?camera=1')
cap = OnlineVideo(url)
# frame_old = np.zeros((480, 640), np.uint8)
# http://192.168.0.108:8080/video.mjpg
while(True):
    frame = cap.getFrame()
    # if frame == None:
    #     # frame = np.zeros((480, 640), np.uint8)
    #     frame = frame_old
    # frame_old = frame
    # time.sleep(.01)
    # print np.shape(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
    elif cv2.waitKey(1) & 0xFF == ord('r'):
        cap = OnlineVideo(url)
        print('retarting')
cv2.destroyAllWindows()
