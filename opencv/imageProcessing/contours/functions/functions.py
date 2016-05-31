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

for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(img, start, end, [0, 255, 0], 2)
    cv2.circle(img, far, 5, [0, 0, 255], -1)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Point Polygon Test
# finds shortest distance between image and a contour
# returns dist which is neg when pt is outside contour, pos when inside contour, zero if on contour
# ex. check pt (50,50)
# 3rd arg is measureDist. True --> finds signed distance; False --> finds whether pt is inside or outside or on contour (returns +1, -1, 0)
# NOTE: if don't want dist, make 3rd arg False, b/c its time consuming process
    # False -> 2-3x speedup

# Match Shapes
# function cv2.matchShapes() enables comparison of 2 shapes or 2 contours
    # returns metric showing similarity
    # lower the result -> better the match
# calculated based on hu-moment values
# different measurement methods explained in the docs

import cv2
import numpy as np

img1 = cv2.imread('star.jpg', 0)
img2 = cv2.imread('star2.jpg', 0)

ret, thresh = cv2.threshold(img1, 127, 255, 0)
ret, thresh2 = cv2.threshold(img2, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, 2, 1)
cnt1 = contours[0]
contours, hierarchy = cv2.findContours(thresh2, 2, 1)
cnt2 = contours[0]

ret = cv2.matchShapes(cnt1, cnt2, 1, 0.0)
print ret

# Hu-Moments seven moments invariant to translation, rotation, and scale
#   7th one is skew-invariant
# see cv2.HuMoments() function

# SEE: docs for cv2.pointPolygonTest()
# cv2.matchShapes() - simple step towards OCR
