"""
Camshift

problem with meanshift: window always has same size when car (in example) is farther away and is very close to camera
    not good
need to adapt window size with size and rotation of target
    solution from OpenCV Labs
CAMshift - continously adaptive meanshift by Gary Bradsky

applies meanshift first
    once converges, updates size of the window as
        s = 2 * sqrt(M_00 / 256)
    also calculates orientation of best fitting ellipse to it
    again applies meanshift with new scaled search window and previous window location
    process continues until required accuracy is met
"""

# Camshift in OpenCV
# almost same as meanshift
    # but returns rotated rectangle (our result)
    # and box parameters (pased as search window in next iteration)

import numpy as np
import cv2

cap = cv2.VideoCapture('slow.flv')

# take first frame of the video
ret, frame = cap.read()

# setup initial location of window
r, h, c, w = 250, 90, 400, 125 # simply hardcoded values
track_window = (c, r, w, h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# setup the termination criteria; either 10 iterations or move by at least 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret, frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # apply meanshift to get the new location
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # draw it on the image
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv2.polylines(frame, [pts], True, 255, 2)

        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg", img2)
    else:
        break
cv2.destroyAllWindows()
cap.release()
