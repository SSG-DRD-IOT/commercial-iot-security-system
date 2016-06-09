import numpy as np
import cv2
from matplotlib import pyplot as plt

selecting = False
dx = 5
dy = 5
def regionSelect(event, x, y, flags, param):
    global xi, yi, xf, yf, selecting, roiHist, dx, dy
    if event == cv2.EVENT_LBUTTONDOWN:
        plt.close('all')
        selecting = True
    elif event == cv2.EVENT_LBUTTONUP:
        selecting = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if selecting==True:
            roiHist = cv2.calcHist([hsv[x-dx:x+dx, y-dy:y+dy]], [0, 1], None, [180, 256], [0, 180, 0, 256])
            imshow('Histogram', roiHist)


img = imread('colorful.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


cv2.namedWindow('Colors')
cv2.setMouseCallback('Colors', regionSelect)
# roiHist = np.zeros((180, 256), np.uint8)
#
# while(True):
#     _, frame = cap.read()
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     mask = np.zeros(frame.shape[:2], np.uint8)
#
#     mask[min(yi, yf):max(yi, yf), min(xi, xf):max(xi, xf)] = 255
#     roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
#
#     targetHist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
#
#     dst = cv2.calcBackProject([hsv], [0, 1], roiHist, [0, 180, 0, 256], 1)
#     disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
#     cv2.filter2D(dst, -1, disk, dst)
#     prox = np.copy(dst)
#
#     # threshold and binary AND
#     _, thresh = cv2.threshold(dst, 50, 255, 0)
#
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
#
#     thresh = cv2.erode(thresh, kernel, iterations = 3)
#     thresh = cv2.dilate(thresh, kernel, iterations= 4)
#
#     masked_dots = cv2.bitwise_and(prox, prox, mask = thresh)
#
#     prox = cv2.applyColorMap(prox, cv2.COLORMAP_JET)
#
#     cv2.imshow('mask', mask)
#     cv2.imshow('frame', frame)
#     cv2.imshow('roiHist', roiHist)
#     cv2.imshow('tHist', targetHist)
#     cv2.imshow('threshold map', thresh)
#     cv2.imshow('distance', prox)
#     cv2.imshow('maskedDots', masked_dots)
#
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
# plt.close('all')
# cap.release()
# cv2.destroyAllWindows()
cv2.waitKey(0)
cv2.destroyAllWindows()
