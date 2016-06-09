"""
Countours - start
finding, drawing contours
functions:
cv2.
    findContours()
    drawContours()
"""

# Countours
# a curve joining all continuous points along the boundary, having same color or intensity
    # useful for shape analysis and object detection/recognition
# for btter accuracy, use binary images
    # before finding contours, apply threshold or canny edge detection
# findContours function modifies src image - if want src img after finding contours, store it to some other vars
# finding contours like finding white object from black bg

# ex. find contours of binary image
import numpy as np
import cv2

im = cv2.imread('test.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 3 args to cv2.findContours():
    # src image
    # contour retrieval mode
    # contour approximation method
# outputs contours and hierarchy
    # contours - python list of all contours in image
        # each indiv contour is Numpy array of (x,y) coords with boundary pts of object

# Drawing contours
# use cv2.drawContours function
# can draw any shape, provided you have its boundary points
    # arguments: src img, contours passed as Python list, index of contours (useful for indiv contour; for all contours, pass -1), color, thickness, ...

# draww all the contours of an image:
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

# draw indiv contour, ex. the 4th contour
cv2.drawContours(img, contours, 3, (0, 255, 0), 3)

# most of the time, more useful method:
cnt = contours[4]
cv2.drawContours(img, [cnt], 0, (0, 255, 0), 3)


# Contour Approximation Method
# pass cv2.CHAIN_APPROX_NONE, all the boundary pts are stored - BUT not all are necessarily needed
# ex. if line, cv2.CHAIN_APPROX_SIMPLE removes all redundant pts and compresses the contour, saving memory
