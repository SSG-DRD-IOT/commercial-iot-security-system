"""
drawing geometric shapes with openCV
cv.
    line()
    circle()
    rectangle()
    ellipse()
    putText()
common arguments:
    -img - image where you draw shapes
    -color - color of shape; BGR=tuple, grayscale=scalar
    -thickness - of line or circle; default=1
    -lineType - default 8-connected, cv2.LINE_AA anti-aliased, great for curves
"""

# draw a line - pass start, end coords
import numpy as np
import cv2

# create a black image
img = np.zeros((512, 512, 3), np.uint8)

# draw a diagonal blue line with thickness of 5 px
cv2.line(img, (0,0), (511, 511), (255, 0, 0), 5)
# ^ (img, coordInit, coordFin, color, thickness)

# draw rectangle
cv2.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3)

# draw circle - need center coords and radius; draw inside rectangle above
cv2.circle(img, (447, 63), 63, (0,0,255), -1)

# draw ellipse - center location, axis lengths (major, minor), angle of rotation in ccw, startAngle and endAngle -- start and end of ellipse arc cw from major axis
# i.e. 0 and 360 gives full ellipse
cv2.ellipse(img, (256, 256), (100, 50), 0, 0, 180, 255, -1)

# draw polygon - first need vertical coords; points in array of shape ROWSx1x2 (rows=#vertices, type int32)
pts = np.array([[10,5], [20,30], [70,20], [50,10]], np.int32)
pts = pts.reshape((-1, 1, 2))
print pts
cv2.polylines(img, [pts], True, (0, 255, 255))

# cv2.polylines(img, [pts], True, (0, 255, 255))
# ^ if arg 3 is False, polylines join all pts, not closed shape
# cv2.polylines() can draw multiple lines; all drawn individually

# add text to image - text data, position coords (bottom left corner), font type, font scale, color, thickness, linType, ...
#   linType=cv2.LINE_AA recommended
# write in white color:
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV', (10,500), font, 4, (255, 255, 255), 2, cv2.LINE_AA)

cv2.imshow('image', img)
cv2.waitKey(0)
