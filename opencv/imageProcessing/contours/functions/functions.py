"""
More Functions
convexity defects and how to find them
finding shortest distance from a point to a polygon
matching different shapes
"""

# Convexity Defects
# any deviation of object from convex hull is a convexity defect
# openCV has ready-made function to find these: cv2.convexityDefects()
hull = cv2.convexHull(cnt, returnPoints = False) # pass returnPoints=False in order to find convexity defects
defects  cv2.convexityDefects(cnt, hull)
# returns array where each row contains values: [start pt, end pt, farthest pt, approx dist to farthest pt]
    # visualize using image - draw line joining start pt and end pt, then draw circle at farthest pt
    # 1st 3 vals are indices of cnt so bring vals from cnt

import cv2
import numpy as np

img = cv2.imread('star.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, 2, 1)
cnt = contours[0]

hull = cv2.convexHull(cnt, returnPoints = False)
defects = cv2.convexityDefects(cnt, hull)
