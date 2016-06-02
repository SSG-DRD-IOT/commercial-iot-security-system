"""
Display three views:
    original frame
    mask
    resultant frame
whenever user clicks in original frame, color is specified
this color becomes the new mask color
The system then creates a contour around the largest object of that color on the screen, and a crosshair follows after that object
"""

import cv2
import numpy as np

color = np.array([0,0,0])
# CRAN = 20
# CRanArr = np.array([20, 10, 10])
# try (0, 50, 10)
def findHSV(bgr):
    "convert BGR array to HSV"
    bgr = np.uint8([[bgr]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    return hsv

def drawXHair(img, y, x):
    # 20 pt radius
    color = (0,0,255)
    # color = tuple(col[0][0])
    # print type(col)
    # print(col)
    radius = 20
    thickn = 2
    cv2.circle(img, (int(x), int(y)), 20, color, thickn)
    cv2.line(img, (x-radius, y), (x+radius, y), color, thickn)
    cv2.line(img, (x, y-radius), (x, y+radius), color, thickn)


def colorSelect(event, x, y, flags, param):
    global color
    if event == cv2.EVENT_LBUTTONUP:
        color_rgb = frame[y, x, 0:3]
        color = findHSV(color_rgb)
        print(color)

def doNothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', colorSelect)

cv2.namedWindow('trackbars')
cv2.createTrackbar('H', 'trackbars', 0, 50, doNothing)
cv2.createTrackbar('S', 'trackbars', 50, 50, doNothing)
cv2.createTrackbar('V', 'trackbars', 10, 50, doNothing)
while(1):
    dh = cv2.getTrackbarPos('H', 'trackbars')
    ds = cv2.getTrackbarPos('S', 'trackbars')
    dv = cv2.getTrackbarPos('V', 'trackbars')
    CRanArr = np.array([dh, ds, dv])
    # take each frame
    _, frame = cap.read()
    print(np.shape(frame))
    # convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    # lower_color = color + np.array([-CRAN, -CRAN, -CRAN])
    # upper_color = color + np.array([CRAN, CRAN, CRAN])
    lower_color = color - CRanArr
    upper_color = color + CRanArr
    # print lower_color , '|' , upper_color
    # threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Noise removal experimentation
    kernel = np.ones((20,20), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # mask = cv2.erode(mask, kernel, iterations = 1)
    # mask = cv2.dilate(mask, kernel, iterations=5)

    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(mask, contours, -1, 150,  3)

    area = 0
    largest_contour = 0
    for i in xrange(len(contours)):
        if cv2.contourArea(contours[i])>area:
            largest_contour = i

    cv2.drawContours(mask, contours, largest_contour, 150,  3)
    print len(contours)
    if len(contours)>0:
        M = cv2.moments(contours[largest_contour])
        if M['m00']>0:
            cx = int(M['m10']/(M['m00']))
            cy = int(M['m01']/(M['m00']))
            print cx ,'|', cy
            drawXHair(frame, cy, cx)
            print(color)
    # bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask= mask)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
