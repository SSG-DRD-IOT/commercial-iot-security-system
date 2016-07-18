import numpy as np
import cv2

def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist

cv2.namedWindow('frame')
cv2.namedWindow('dist')

cap = cv2.VideoCapture(0)

_, frame1 = cap.read()
_, frame2 = cap.read()

while(True):
    _, frame3 = cap.read()
    dist = distMap(frame1, frame3)

    cv2.imshow('frame', frame2)

    frame1 = frame2
    frame2 = frame3


    cv2.imshow('dist', dist)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
