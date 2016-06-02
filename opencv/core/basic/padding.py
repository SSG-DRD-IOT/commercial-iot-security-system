"""
making borders for images - padding
create a border around the image (like photo frame) - cv2.copyMakeBorder()
    - has more apps for convolution operation, zero padding, etc.
function arguments for cv2.copyMakeBorder() :
    - src - input image
    - top, bottom, left, right - border width in # of pixels in corresponding directions
    - borderType - flag defining what kind of border to be added. Can have following types:
        - cv2.
            BORDER_CONSTANT - adds a constant colored border. value given as next argument
            BORDER_REFLECT - border will be mirror reflection of the border elements, like this:
                fedcba|abcdefgh|hgfedcb
            BORDER_REFLECT_101 or BORDER_DEFAULT - same as above, but with slight change:
                gfedcb|abcdefgh|gfedcba
            BORDER_REPLICATE - last element is replicated throughout, like this:
                aaaaaa|abcdefgh|hhhhhhh
            BORDER_WRAP - looks like:
                cdefgh|abcdefgh|abcdefg
    - value - color of border if border type is cv2.BORDER_CONSTANT
"""

# example code for border types
import cv2
import numpy as np
from matplotlib import pyplot as plt

BLUE = [255, 0, 0]

img1 = cv2.imread('opencv_logo.png')

replicate = cv2.copyMakeBorder(img1, 10, 10, 10, 10, cv2.BORDER_REPLICATE)
reflect = cv2.copyMakeBorder(img1, 10, 10, 1, 10, cv2.BORDER_REFLECT)
reflect101 = cv2.copyMakeBorder(img1, 10, 10, 10, 10, cv2.BORDER_REFLECT_101)
wrap = cv2.copyMakeBorder(img1, 10, 10, 10, 10, cv2.BORDER_WRAP)
constant = cv2.copyMakeBorder(img1, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=BLUE)

plt.subplot(231), plt.imshow(img1, 'gray'), plt.title('ORIGINAL')
plt.subplot(232), plt.imshow(replicate, 'gray'), plt.title('REPLICATE')
plt.subplot(233), plt.imshow(reflect, 'gray'), plt.title('REFLECT')
plt.subplot(234), plt.imshow(reflect101, 'gray'), plt.title('REFLECT_101')
plt.subplot(235), plt.imshow(wrap, 'gray'), plt.title('WRAP')
plt.subplot(236), plt.imshow(constant, 'gray'), plt.title('CONSTANT')

plt.show()
