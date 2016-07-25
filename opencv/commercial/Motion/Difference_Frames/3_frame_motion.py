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

cap = cv2.VideoCapture("cars.avi")

_, frame1 = cap.read()
_, frame2 = cap.read()

while(True):
    _, frame3 = cap.read()
    dist = distMap(frame1, frame3)
    # cv2.imshow('dist', dist)
    cv2.imshow('frame', frame2)

    frame1 = frame2
    frame2 = frame3

    # apply Gaussian blurring
    mod = cv2.GaussianBlur(dist, (9,9), 0)
    # apply thresholding
    _, thresh = cv2.threshold(mod, 100, 255, 0)
    edge = cv2.Canny(thresh, 100, 200)
    # apply closing
    kernel = np.ones((3,3), np.uint8)
    kernel2 = np.ones((2,2), np.uint8)
    closed = cv2.erode(thresh, kernel, iterations = 1)
    closed = cv2.dilate(closed, kernel2, iterations = 10)
    # closed = cv2.dilate(thresh, kernel, iterations = 20)
    # closed = cv2.erode(closed, kernel, iterations = 10)
    # edge = cv2.Canny(closed, 100, 200)
    # mod = closed
    # mod = edge

    # mean and st dev test
    mean, stDev = cv2.meanStdDev(mod)
    print stDev
    cv2.imshow('dist', mod)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
