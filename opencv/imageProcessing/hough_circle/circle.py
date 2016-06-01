"""
Hough Circle Transform
- find circles in an image
function: cv2.HoughCircles()

circle represented mathematically as (x - x_center)^2 + (y - y_center)^2 = r^2
    (x_center, y_center) is center of circle
    r is radius of circle
3 parameters -> need 3D accumulator for hough transform
    likely ineffective
OpenCV uses Hough Gradient method
    uses gradient info of edges
function is cv2.HoughCircles()
    many arguments; see documentation
"""

import cv2
import numpy as np

img = cv2.imread('opencv_logo.png', 0)
img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, param2 = 30, minRadius = 0, maxRadius = 0)

circles = np.uint8(np.around(circles))
for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
