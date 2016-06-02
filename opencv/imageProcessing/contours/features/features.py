"""
finding different features of contours, like area, perimeter, centroid, bounding box, etc.
plenty of functions related to contours
"""

# Moments
# image moments - calculate features like center of mass of object, object area, etc.
# function: cv2.moments() - gives dictionary of all moments calculated
import numpy as np
import cv2

img = cv2.imread('star.jpg', 0)
ret, thresh = cv2.threshold(img, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]
M = cv2.moments(cnt)
print M

# from moments, extract data like area, centroid, etc.
# centroid given by relations:
    # C_x = M_10 / M_00
    # C_y = M_01 / M_00
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

# Contour Area
# from function cv2.contourArea() or from moments, M['m00']
area = cv2.contourArea(cnt)

# Contour Perimeter
# also called 'arc length'
# use cv2.arcLength()
    # 2nd argument specifies whether shape is closed contour (True) or just a curve
perimeter = cv2.arcLength(cnt, True)

# Contour Approximation
# approximates a contour shape to another shape with less vertices, depending upon specified precision
# implements Douglas-Peucker algorithm
# ex. try to find square in image, but have imperfect square, 'bad shape'
# use function to approximate shape
    # 2nd argument: epsilon; max distance from contour to approximated contour - accuracy parameter
epsilon = 0.1*cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)

# Convex Hull
# looks similar to contour approximation (but isn't)
# cv2.convexHull() checks curve for convexity defects and corrects it
# convex curves are curves which are always bulged out or at least flat
    # bulged inside - convexity defect
    # convexity defects are local max deviations of hull from contours
# hull = cv2.convexHull(points[, hull[, clockwise[, returnPoints]]])
# argument details:
    # points - contours we pass into
    # hull - output, normally avoided
    # clockwise - orientation flag; True -> output convex hull oriented cw; otw, orientated ccw
    # returnPoints - True by default ->returns coords of hull pts; false -> ret indices of contour pts corresponding to hull pts
# so sufficient to get the convex full of hand image:
hull = cv2.convexHull(cnt)
# for convexity defects, pass returnPoints=False

# Checking Convexity
# function cv2.isContourConvex() checks whether contour is convex or not, returns True or False
k = cv2.isContourConvex(cnt)

# Bounding Rectangles - 2 types
    # straight bounding rectangle - doesn't consider object rotation, so area of bounding rect won't be minimum
    # function: cv2.boundingRect()
    # (x,y) top-left coord of the rect, (w,h) width and height
x, y, w, h = cv2.boundingRect(cnt)
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # rotated rectangle - bounding rect is drawn with min area, so also considers rotation
    # returns Box2D structure with following details - (center (x,y), (width, height), angle of rotation)
    # to draw rect, need 4 corners - obtained using cv2.boxPoints()
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

# Minimum Enclosing Circle
# function: cv2.minEnclosingCircle() - circle which completely covers object w/ min area
(x,y), radius = cv2.minEnclosingCircle(cnt)
center = (int(x), int(y))
radius = int(radius)
cv2.circle(img, center, radius, (0, 255, 0), 2)


# Fitting an Ellipse
# returns rotated rectangle in which ellipse is inscribed
ellipse = cv2.fitEllipse(cnt)
cv2.ellipse(img, ellipse, (0, 255, 0), 2)

# Fitting a Line
# can fit a line to a set of points
# ex. if image contains a set of white points, approximate a straight line to it:
rows, cols = img.shape[:2]
[vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vs)+y)
cv2.line(img, (cols-1, righty), (0, lefty), (0, 255, 0), 2)
