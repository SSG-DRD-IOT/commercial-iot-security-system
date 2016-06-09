"""
find objects in an image using Template Matching
cv2.matchTemplate(), cv2.minMaxLoc()

template matching - method for searching and finding the location of a template in a larger image
    OpenCV uses cv2.matchTemplate() for this purpose
        slides template image over input image (2D Convolution), compares template and patch of input image under template image
        several comparisons implemented in OpenCV
    returns grayscale img, where each pixel denotes match of nbhd of pixel w/ template
    input img of size(WxH) and template img of size (wxh) output img of size (W-w+1, H-h+1)
        after result, use cv2.minMaxLoc() function to find where min/max value
    take at top-left corener of rectangle, take (w,h) as width and ht of rectangle
        this rectangle is the region of template
"""
# NOTE: if using cv2.TM_SQDIFF as comparison method, min value gives the best match

# Template matching in OpenCV

# ex. search for Messi's face in photo
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('messi5.jpg', 0)
img2 = img.copy()
template = cv2.imread('template.jpg', 0)
w, h = template.shape[::1]

# all the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # apply template matching
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # if method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img, top_left, bottom_right, 255, 2)

    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.subtitle(meth)

    plt.show()
