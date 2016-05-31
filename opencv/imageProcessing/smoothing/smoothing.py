"""
Image blurring (image smoothing)
Image blurring - convolve image with LPF
useful for
    removing noises (high freq content) - (eg noise, edges) from image
        so edges blurred a bit in operation

Blurring techniques:
"""

# Averaging
    # convolving image with normalized box filter
    # takes average of all pixels under kernel area, replaces with central element
    # function: cv2.blur() and cv2.boxFilter()
        # specify width and height of kernel
    # NOTE: if don't want normalized, use cv2.boxFilter() with argument normalize=False
# kernel of 5x5 size example:
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('opencv_logo.png')

blur = cv2.blur(img, (5,5))

plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(blur), plt.title('Blurred')
plt.xticks([]), plt.yticks([])
plt.show()

# Gaussian Blurring
    # instead of box filter, use Gussian kernel
    # function: cv2.GaussianBlur()
        # specify width, height of kernel which should be pos and odd
        # also std deviation in X and Y dir, sigmaX and sigmaY
            # if only sigmaX specified, sigmaY=sigmaX
            # both 0s, calculated from kernel size
        # highly effective in removing gaussian noise from image
    # create Gaussian kernel with function cv2.getGaussianKernel()

# modify above code for Gaussian blurring:
blur = cv2.GaussianBlur(img, (5,5), 0)

# Median Blurring
    # function: cv2.medianBlur() - takes median of all pixels under kernel area & central element is replaced w/ median value
    # highly effective against salt-and-pepper noise in images
        # in median blurring, central element ALWAYS replaced with some pixel value in image
            # reduces noise effectively
            # kernel size is a pos integer
median = cv2.medianBlur(img, 5)

# Bilateral Filtering
    # cv2.bilateralFilter() highly effective in noise removal while keeping edges sharp, BUT operation slower compared to other filters
    # Bilateral filter takes Gaussian filter in space, but one more gaussian filter, a function of filter of pixel difference
        # Gaussian function of space assures only nearby pixels considered for blurring
        # while gaussian function of intensity difference assures only pixels with similar intensity to central pixel is considered for blurring
            # preserves edges since pixels @ edges have large intensity variation
blur = cv2.bilateralFilter(img, 9, 75, 75)
# SEE: http://people.csail.mit.edu/sparis/bf_course/
