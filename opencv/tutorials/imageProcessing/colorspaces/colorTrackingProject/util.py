import numpy as np
import cv2

def findHSV(bgr):
    "convert BGR array to HSV"
    bgr = np.uint8([[bgr]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    return hsv

# for graphics
def drawXHair(img, y, x):
    # 20 pt radius
    color = (0,0,0)
    radius = 20
    thickn = 2
    cv2.circle(img, (int(x), int(y)), 20, color, thickn)
    cv2.line(img, (x-radius, y), (x+radius, y), color, thickn)
    cv2.line(img, (x, y-radius), (x, y+radius), color, thickn)
