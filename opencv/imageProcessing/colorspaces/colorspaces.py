"""
convert images from one colorspace to another, like BGR <-> Gray, BGR <-> HSV, ...
create application which extracts colored object in a video
cv2.cvtColor(), cv2.inRange(), etc.
"""
# Changing Color Spaces

# 150+ color space conversion methods available; most widely used ones are BGR<->Gray and BGR<->HSV
# for color conversion, ue function cv2.cvtColor(input_image, flag) where flag determines type of conversion
# for BGR -> Gray, use flags cv2.COLOR_BGR2GRAY
# for BGR -> HSV, use flag cv2.COLOR_BGR2HSV

# to get other flags:
import cv2
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
print flags

# NOTE: for HSV, Hue range [0, 179], Saturation range [0,255], Value range [0, 255]
# different softwares use different scales --> if comparing OpenCV vals with them, normalize ranges


# Object Tracking
# can convert BGR image to HSV --> can now extract a colored object
# in HSV, easier to represent a color than in BGR colorspace

# try to extract blue object
# method:
# - take each frame of the video
# - convert from BGR to HSV colorspace
# -threshold HSV image for a range of blue color
# extract blue object alone; can do whatever to the image we want

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):
    # take each frame
    _, frame = cap.read()

    # convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # -----test-----
    # Noise removal experimentation
    # kernel = np.ones((3,3), np.uint8)
    kernel = np.ones((5,5), np.uint8)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.erode(mask, kernel, iterations = 1)
    mask = cv2.dilate(mask, kernel, iterations=5)
    # -----/test----

    # bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask= mask)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
