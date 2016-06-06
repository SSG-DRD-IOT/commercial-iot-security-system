import numpy as np
import cv2

xi, yi, xf, yf = 0, 0, 0, 0
selecting = False
foo = False
# bar = False
def regionSelect(event, x, y, flags, param):
    # print(selecting)
    global xi, yi, xf, yf, selecting, foo, roiHist #, bar
    if event == cv2.EVENT_LBUTTONDOWN:
        selecting = True
        xi, yi = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        selecting = False
        foo = True
        xf, yf = x, y
        # mask[min(yi, yf):max(yi, yf), min(xi, xf):max(xi, xf)] = 255
        roiHist = cv2.calcHist([hsv], [0, 1], mask, [180, 256], [0, 180, 0, 256])
        # roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)

cap = cv2.VideoCapture(0)
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', regionSelect)

roiHist = np.zeros((180, 256), np.uint8)

while(True):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = np.zeros(frame.shape[:2], np.uint8)

    mask[min(yi, yf):max(yi, yf), min(xi, xf):max(xi, xf)] = 255
    # cv2.rectangle(frame, (xi, yi), (xf, yf), (255, 0, 0), 3)
    # roiHist = cv2.calcHist([hsv], [0, 1], mask, [180, 256], [0, 180, 0, 256])
    roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)

    targetHist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

    dst = cv2.calcBackProject([hsv], [0, 1], roiHist, [0, 180, 0, 256], 1)
    disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    cv2.filter2D(dst, -1, disk, dst)

    # threshold and binary AND
    # ret, thresh = cv2.threshold(dst, 50, 255, 0)
    ret, thresh = cv2.threshold(dst, 230, 255, 0)
    kernel = np.ones((20,20), np.uint8)
    # kernel = disk
    # threshold = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    thresh = cv2.erode(thresh, kernel, iterations = 1)
    thresh = cv2.dilate(thresh, kernel, iterations= 2)

    # thresh = cv2.merge((thresh, thresh, thresh))
    # res = cv2.bitwise_and(frame, thresh)
    cv2.imshow('mask', mask)
    # display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('roiHist', roiHist)
    cv2.imshow('tHist', targetHist)
    cv2.imshow('threshold map', thresh)
    # cv2.imshow('dst', dst)

    if cv2.waitKey(1) & 0xFF == 27:
        break
# when everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
