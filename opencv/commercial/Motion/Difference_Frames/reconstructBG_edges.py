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

def frameAvg(prevLen, prevAvg, frame):
    frame_64 = np.float64(frame)
    prevAvg = np.float64(prevAvg)
    prevSum = prevLen * prevAvg
    newLen = prevLen + 1
    # cv2.accumulate(prevSum, )
    newAvg_64 = (frame_64 + prevSum) / newLen
    newAvg = np.uint8(newAvg_64)
    # print newAvg
    return newLen, newAvg


# cv2.namedWindow('frame')
# cv2.namedWindow('dist')
AVG_LEN = 100 # 70 - background appears; 2 - motion detection; 200
cap = cv2.VideoCapture("cars.avi")
ret, Avg = cap.read()
oldCount = 1
while(True and ret):
    ret, frame = cap.read()
    # Avg = cv2.GaussianBlur(Avg, (5,5), 0)
    # frame = cv2.GaussianBlur(frame, (5,5), 0)
    oldCount, Avg = frameAvg(oldCount, Avg, frame)

    if oldCount >= AVG_LEN:
        oldCount = AVG_LEN
    dist = distMap(frame, Avg)

    cv2.imshow('average', Avg)
    # cv2.imshow('frame', frame)
    # dist = distMap(frame1, frame3)

    # Avg = cv2.cvtColor(Avg, cv2.COLOR_BGR2GRAY) # errors

    blur_road = cv2.GaussianBlur(Avg, (3,3), 0)
    blur_road_gray = cv2.cvtColor(blur_road, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(blur_road, 20, 255) # middle 128
    # _, blurd = cv2.threshold(blurd, 30, 255, 0)

    cv2.imshow("blurred road", blur_road)
    cv2.imshow("blurred road gray", blur_road_gray)

    cv2.imshow("Road edge", edge)

    cv2.imshow('dist', dist)
    # cv2.imshow('blurred', blurd)

    _, thresh = cv2.threshold(dist, 65, 255, 0)
    cv2.imshow('thresh', thresh)

    # kernel = np.ones((3,3), np.uint8)
    # kernel2 = np.ones((2,2), np.uint8)
    # closed = cv2.erode(thresh, kernel, iterations = 1)
    # closed = cv2.dilate(closed, kernel2, iterations = 30)
    # cv2.imshow("closed", closed)

    if cv2.waitKey(1) & 0xFF == 27:
        break
print "video finished"
cap.release()
cv2.destroyAllWindows()
