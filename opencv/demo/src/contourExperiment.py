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

def findHSV(bgr):
    "convert BGR array to HSV"
    bgr = np.uint8([[bgr]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    return hsv

def drawXHair(img, y, x):
    "draws crosshair at specified point"
    color = (0,0,255)
    radius = 20
    thickn = 2
    cv2.circle(img, (int(x), int(y)), 20, color, thickn)
    cv2.line(img, (x-radius, y), (x+radius, y), color, thickn)
    cv2.line(img, (x, y-radius), (x, y+radius), color, thickn)


def colorSelect(event, x, y, flags, param):
    "click to select color"
    global color
    if event == cv2.EVENT_LBUTTONUP:
        color_rgb = frame[y, x, 0:3]
        color = findHSV(color_rgb)
        print(color)

def doNothing(x):
    "does nothing"
    pass

# begin the video capture
cap = cv2.VideoCapture(0)
cv2.namedWindow('Track Color Object')
cv2.setMouseCallback('Track Color Object', colorSelect)

cv2.createTrackbar('H', 'Track Color Object', 0, 50, doNothing)
cv2.createTrackbar('S', 'Track Color Object', 50, 50, doNothing)
cv2.createTrackbar('V', 'Track Color Object', 10, 50, doNothing)
while(1):
    dh = cv2.getTrackbarPos('H', 'Track Color Object')
    ds = cv2.getTrackbarPos('S', 'Track Color Object')
    dv = cv2.getTrackbarPos('V', 'Track Color Object')

    # create the color range array from these values
    cRanArr = np.array([dh, ds, dv])
    # take each frame
    _, frame = cap.read()
    print(np.shape(frame))
    # convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of  color in HSV

    lower_color = color - cRanArr
    upper_color = color + cRanArr

    # threshold the HSV image to only get colors wi specified range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Morphological Noise Removal
    kernel = np.ones((20,20), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # find contours from the mask
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # detect the largest contour
    area = 0
    largest_contour = 0
    for i in xrange(len(contours)):
        if cv2.contourArea(contours[i])>area:
            largest_contour = i

    # draw the largest contour on the mask
    # cv2.drawContours(mask, contours, largest_contour, 150,  3)

    # if contours are available, draw a crosshair on the centroid of the largest contour
    if len(contours)>0:
        # find moment of contour
        M = cv2.moments(contours[largest_contour])
        if M['m00']>0:
            # find contour centroid
            cx = int(M['m10']/(M['m00']))
            cy = int(M['m01']/(M['m00']))
            print cx ,'|', cy
            drawXHair(frame, cy, cx)
            print(color)

    # use bitwise_and to apply mask to original image
    # res = cv2.bitwise_and(frame, frame, mask= mask)
    cv2.imshow('Track Color Object', frame)
    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)

    # if user presses escape key, exit
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
