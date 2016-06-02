import numpy as np
import cv2
# from onlinevid import OnlineVideo
# import time
# cap = OnlineVideo('http://174.51.161.11/mjpg/1/video.mjpg?camera=1')
cap = cv2.VideoCapture('http://174.51.161.11/mjpg/1/video.mjpg')

# http://192.168.0.108:8080/video.mjpg
while(True):
    _, frame = cap.read()
    print type(frame)
    # if frame == None:
    #     frame = np.zeros((480, 640), np.uint8)
    # time.sleep(.01)
    # print np.shape(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()
