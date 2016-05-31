"""
Morphological Transformations
 - learn different Morphological operations like Erosion, Dilation, Opening, Closing, ...
functions:
cv2.
    erode()
    dilate()
    morphologyEx()

Theory:
    M.T. are simple operations based on image shape
    normally performed on binary images
    2 inputs: one is original img, 2nd is "structuring element" or "kernel", decides nature of operation
    2 basic operations:
        erosion
        dilation
    variant forms:
        opening
        closing
        gradient
"""

# Erosion
# erodes away the boundaries of foreground object; (try to keep foreground in white)
# kernel slides thru img, as in 2D conv
# pixel in orig img (1 or 0) considered 1 only if all pixels under the kernel 1, otw eroded (made zero)

# so all pixels near boundary discarded dep. on kernel size
    # thus thickness or size of foreground obj decreases or simply white image decreases in the img
# useful for removing small white noises (as in colorspace chap), detacch 2 connected objects, ...

# ex. 5x5 kernel full of 1's
import cv2
import numpy as np

img = cv2.imread('j.png', 0)
kernel = np.ones((5,5), np.uint8)
erosion = cv2.erode(img, kernel, iterations = 1)

# Dilation
# opposite of erosion
# pixel element is 1 if at least one pixel under kernel is 1
# increases the white region in image or size of foreground img increases
# normally in noise removal, erosion is followed by dilation
    # erosion removes white noises, but also shrinks object - so we dilate it
        # since noise is gone, it won't come back, but object area increases
        # also useful for joining broken parts of an object
dilation = cv2.dilate(img, kernel, iterations=1)

# Opening
# erosion followed by dilation
# useful for removing noise
# function: cv2.morphologyEx()
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# Closing
# reverse of opening: dilation followed by erosion
# useful for closing small holes inside foreground objects or small black pts on the object
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# Morphological Gradient
# difference between dilation and erosion of an image
# result looks like outline of object
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

# Top Hat
# difference between input image and opening the image
# ex. for 9x9 kernel
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

# Black Hat
# difference between closing the input image and input image
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

# Structuring Element
# manually, we created structuring elements with help of Numpy in rectangular shape; but sometimes you need elliptical or circular kernels
# function: cv2.getStructuringElement()
    # pass shape and size of kernel, get desired kernel

# rectangular kernel
cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

# Elliptical Kernel
cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

# Cross-shaped Kernel
cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))

# SEE: http://homepages.inf.ed.ac.uk/rbf/HIPR2/morops.htm
