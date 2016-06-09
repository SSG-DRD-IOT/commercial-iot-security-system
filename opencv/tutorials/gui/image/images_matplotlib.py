"""
display images using Matplotlib
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('messi5.jpg', 0)
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([]) # to hide tick vals on x and y axis
plt.show()

# NOTE: OpenCV is BGR, Matplotlib is RGB
