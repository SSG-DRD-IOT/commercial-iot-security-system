"""
Shi-Tomasi Corner Detector and Good Features to Track

function: cv2.goodFeaturesToTrack()

By Shi and Tomasi in paper Good Features to Track
instead of R = \lambda_1 * \lambda_2 - k(lambda_1 + \lambda_2)^2
    use:
    R = min(\lambda_1 , \lambda_2)

If greater than threshold value, considered corner
see: http://docs.opencv.org/3.1.0/shitomasi_space.png
Only when \lambda_1 and \lambda_2 above a minimum value, \lambda_min is considered a corner
"""

# OpenCV has function cv2.goodFeaturesToTrack()
    # finds N strongest corners in the image by Shi-Tomasi method (or Harris, if specified)
    # image must be grayscale
    # specify # of corners you want to find
    # specify quality level
        # value between 0 and 1
            # denotes min quality of corner below which all is rejected
    # provide min euclidean distance between corners detected

# with ^ info, finds corners in image
    # all corners below quality lvl rejected
# sorts remaining corners based on quality
    # in descending order
# takes 1st strongest corner, throws away all nearby corners in range of min dist
# returns N strongest corners

# ex. try to find 25 best corners:
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('blox.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
corners = np.int0(corners)

for i in corners:
    x, y = i.ravel()
    cv2.circle(img, (x, y), 3, 255, -1)

plt.imshow(img), plt.show()
