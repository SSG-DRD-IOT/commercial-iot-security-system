"""
Hough Line Transform

- convept of Hough Transform
- use it to detect lines in i
functions:
cv2.
    HoughLines()
    HoughLinesP()

HT popular technique to detect any shape, if shape can be represented in mathematical form
    can detect shapes even if broken or distorted
represent line as:
-) y = mx + b
-) p = x*cos(/th) + y*cos(/th) where p is orthogonal dist from origin to line
    /th is angle formed by this perpendicular line and horiz axis measured CCW
    line passing thru origin:
        p positive
        /th < 180 degrees
    above origin
        /th < 180
    vertical line
        /th = 0
    horiz line
        /th = 90 degrees

HT on lines:
    any line can be represented with (p, /th)
    1) creates 2D array or accumulator to hold vals of 2 params, set to 0 initially
        rows denote p, cols denote /th
    2) size of array depends on accuracy needed
        ex want angles to be 1 degree --> 180 columns
        for p, max dist possible is diagonal length of image
            so taking one pixel accuracy, # rows = diagonal length of image
ex. 100x100 img with horiz line in middle
1) take 1st pt of line - know its (x, y) vals
2) for val eq'n, take vale /th = 0, 1, 2, ..., 180 and check every p you get
3) for every (p, /th) pair, increment val by 1 in our accumulator in its corresponding (p, /th) cells
4) now take 2nd pt on line, do same as above; increment vals in cells corresp to (p, /th) you got
    voting the (p, /th) vals
    at each pt, the cell of beginning value incremented of voted up, while other cells may or may not be
    at end, beginning cell will have max votes
5) if search for max votes, get val (p_0, /th_0) which says that theres line in image a dist p_0 from origin and at angle /th_0 degrees
"""

# Hough Transform in OpenCV
# all above encapsulated in opencv function cv2.HoughLines()
    # returns array of (p, /th) values
        # p in pixels, /th in radians
# parameters:
    # image canny image -> apply threshold or use canny edge detection before finding/applying hough transform
    # p accuracy
    # /th accuracy
    # threshold -> minimum vote it should get to be considered a line
        # remember: #votes depend on #pts on line
        # min length of line that should be detected
import cv2
import numpy as np

img = cv2.imread('dave.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 100*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imwrite('houghlines3.jpg', img)
