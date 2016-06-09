"""
handling mouse events in openCV
cv2.setMouseCallback()
"""
# Simple Demo
# simple application; draw circle on an image when you click on it

# create mouse callback function, executed whenever mouse event takes place
# mouse events
#   left-btn down, left-btn up, left-btn double click, etc
#   gives us coords (x,y) of every mouse event
# list all events available:

import cv2
events = [i for i in dir(cv2) if 'EVENT' in i]
print events

import cv2
import numpy as np

# mouse callback function
def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 100, (255, 0, 0), -1)

# create black image and a window, bind function to window
img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

while(1):
    cv2.imshow('image', img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
