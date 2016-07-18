import numpy as np
import cv2

def distMap(frameList):
    frame1_32 = np.float32(frameList[0])
    frame2_32 = np.float32(frameList[-1])
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist

cv2.namedWindow('frame')
cv2.namedWindow('dist')

dF = 4 # delta of frames

cap = cv2.VideoCapture(0)
frames = []
for i in xrange(dF - 2):
    _, frame = cap.read()
    frames.append(frame)

while(True):
    _, frame = cap.read()
    frames.pop(0)
    frames.append(frame)
    dist = distMap(frames)

    # cv2.imshow('frame', frames[int(round(len(frames)/2.0))])
    cv2.imshow('frame', frames[len(frames)/2])
    cv2.imshow('dist', dist)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
