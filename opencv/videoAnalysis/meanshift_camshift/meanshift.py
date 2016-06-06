"""
[Meanshift and Camshift algorithms and object finding / tracking]

Meanshift

see: http://docs.opencv.org/3.1.0/meanshift_basics.jpg

meanshift intuition:
    given set of points, like pixel distribution, and a small window
        move window to area of maximum pixel density
    take window, find centroid of pts inside window, move center of window to centroid
    iterate doing so, such that the center of window and its centroid fall on same location, or wi small desired error
    finally, obtain window with maximum pixel distribution
        this has the max # of points
    Normally, pass histogram backprojected image and iniitial target location
    when obj moves, movement is reflected in histogram backprojected image
        meanshift algorithm moves our window to new location with maximum density
"""

# Meanshift in OpenCV
# first, need to set up the target
# find its histogram so that we can backproject target on each frame for calculation of meanshift
# need to provide initial location of window
    # for histogram, only Hue is considered
# to avoid false values due to low light, low light values discarded using cv2.inRange()
import numpy as np
import cv2

cap = cv2.VideoCapture('slow.flv')

# take first frame of the video
ret, frame = cap.read()

# setup initial location of window
r, h, c, w = 250, 90, 400, 125 # simply hardcoded values
track_window = (c, r, w, h)

# setup the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# setup the termination criteria, either 10 iteration or move by at least 1 pt
term_crit =  (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while(1):
    ret, frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # draw it on image
        x, y, w, h = track_window
        img2 = cv2.rectangle(frame, (x, y), (x+w, y+h), 255, 2)
        cv2.imshow('img2', img2)

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k) + ".jpg", img2)
    else:
        break
cv2.destroyAllWindows()
cap.release()
