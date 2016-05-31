"""
Adaptive thresholding

when image has different lighting conditions in different areas, simple thresholding no good
Adaptive: algorithm calculates threshold for small regions of image
    - different thresholds for different regions of same image
    - gives better results for images with varying illumination
"""

# 3 special input params, one output param
# adaptive method - how thresholding value calculated
# - cv2.ADAPTIVE_THRESH_MEAN_C - threshold value is mean of nbhd area
# - cv2.ADAPTIVE_THRESH_GAUSSIAN_C - threhold val is weighted sum of nbhd vals
#   weights are a gaussian window
# Block size - decides sum of nbhd area
# C - constant subtracted from mean or weighted mean calculated

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('dave.jpg', 0)
img = cv2.medianBlur(img, 5)

ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
        cv.THRESH_BINARY, 11, 2)
th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
        cv2.THRESH_BINARY, 11, 2)
titles = ['Original Image', 'Global Thresholding (v = 127)', 'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]

for i in xrange(4):
    plt.subplot(2, 2, i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()
