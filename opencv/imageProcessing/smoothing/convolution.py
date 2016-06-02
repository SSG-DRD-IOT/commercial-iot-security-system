"""
Smoothing images
    blur images with various low pass filters
    apply custom-made filters to images (2D Convolution)

2D Convolution (image filtering)
images can be filtered with various low-pass filters (LPF), high-pass filters (HPF), ...
LPF helps remove noises, blur images
HPF filters help find edges in images

function:
cv2.filter2D() - convolve kernel with an image
"""

# 5x5 averaging filter kernel:
# K = (1/25) [1 1 1 1 1;
#             1 1 1 1 1;
#             1 1 1 1 1;
#             1 1 1 1 1;
#             1 1 1 1 1]
# operation: keep kernel above a pixel, add all 25 pixels below the kernel, take the avg, replace central pixel w/ new avg value
# continues operation for all pixels in the image

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('opencv_logo.png')

kernel = np.ones((5,5), np.float32)/25
dst = cv2.filter2D(img, -1, kernel)

plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(dst), plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.show()
