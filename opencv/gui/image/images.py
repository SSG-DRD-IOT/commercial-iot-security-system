"""
read image, display it, save it back
cv2.
    imread()
    imshow()
    imwrite()
display images with matplotlib
"""
# cv.imread() flags: cv2.IMREAD_COLOR (1), GRAYSCALE(0), UNCHANGED(-1)

import numpy as np
import cv2

# load a color image in grayscale
img = cv2.imread('messi5.jpg',0) # warning: if path is wrong, gives None

# cv2.imshow() arguments: window name (string), image; create as many windows a you wish
# as long as each has its own window name

cv2.imshow('image', img)
cv2.waitkey(0) # keyboard binding function; argument is time in millis; waits for specified milliseconds
# for keyboard event. 0 --> waits indef for key stroke
# MUST be used to display image
cv2.destroyAllWindows(); #distroys all created windows
# single window: cv2.destroyWindow(windowname)
# special case: create window and resize later (specify whether resizeable)
# cv2.namedWindow, flag is cv2.WINDOW_AUTORESIZE (default); if specify WINDOW_NORMAL, can resize window

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows

# cv2.imwrite(fname, image_to_save)
cv2.imwrite('messigray.png', img)
