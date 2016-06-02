"""
Probabilistic Hough Transform

    # this is Hough you do it.

    in HT, even for line w/ 2 arguments, lots of computation
Probabilistic Hough Transform is optimization of HT we saw
    only considers random subset of points
        sufficient for line detection
    have to decrease threshold
function: cv2.HoughLinesP()
    2 arguments:
    minLineLength - min length of line; segments shorter than this rejected
    maxLineGap = max allowed gap between line segments to treat them as single line
# directly returns endpts of lines
    previously, only got parameters of lines and had to find all points
    now, all directly given
"""

import cv2
import numpy as np
img = cv2.imread('dave.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
lines = cv2.HoughLinesP(edges, 1, np.pi/180,100,minLineLength=100,maxLineGap=10)
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imwrite('houghlines5.jpg', img)
