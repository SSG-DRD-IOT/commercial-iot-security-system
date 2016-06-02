"""
bind trackbar to openCV windows
cv2.
    getTrackbarPos()
    createTrackbar()
"""

# application shows specified color
# window showing color, 3 trackbars specifying each of BGR colors
# slide trackbar, correspondingly window color changes; default color is Black

# cv2.getTrackbarPos() - trackbar name, window name where attached, default value, max value
# last is callback function executed every time trackbar val changes
# trackbar - use as button or switch
#   no button functionality in openCV by default
#   our app only works if switch is on, otw screen always black

import cv2
import numpy as np

def nothing(x):
    pass

# create a black image, a window
img = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('R', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('B', 'image', 0, 255, nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image', 0, 1, nothing)

while(1):
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    b = cv2.getTrackbarPos('B', 'image')
    s = cv2.getTrackbarPos(switch, 'image')

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b, g, r]
cv2.destroyAllWindows()
