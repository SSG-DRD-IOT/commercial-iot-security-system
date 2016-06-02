"""
Histogram Back-Projection
proposed by Michael Swain, Dana Ballard in Indexing via color histograms

used for image segmentation (finding objects of interest in an image)
creates image of same size but single channel as that of onput image where each pixel corresponds
    to probability of pixel belonging to object
output image has object of interest in more white than remaining part
used with camshift algorithm

-> create histogram of image containing object of interest
    obj should fill image as far as possible for best results
color histogram preferred over grayscale histogram b/c color of object is better way to define obj than grayscale intensity
then, 'back-project' histogram over test image where we need to find object
    ie calculate probability of every pixel belonging to ground and show it
resulting output on proper thresholding gives the ground alone
"""
# Algorithm in Numpy
# 1st, calculate the color histogram of both object we need to find, 'M', and image where we search, 'I'
import cv2
import numpy as np
from matplotlib import pyplot as plt

# roi is the object or region of object we need to find
roi = cv2.imread('rose_red.png')
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# target is the image we search in
target = cv2.imread('rose.png')
hsvt = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)

# find the histograms using calcHist; can be done with np.histogram2d also
M = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
I = cv2.calcHist([hsvt],[0, 1], None, [180, 256], [0, 180, 0, 256] )

# find ratio R = M/I, then backproject R ie use R as paletter and create new image w/ every pixel as its corresponding probabily
#   of being target
    # ie B(x,y) = R[h(x,y), s(x,y)] h is hue, s is saturation of pixel @ (x,y)
    # then, apply condition B = min(B(x,y), 1)
h, s, v = cv2.split(hsvt)
B = R[h.ravel(), s.ravel()]
B = np.minimum(B, 1)
B = B.reshape(hsv.shape[:2])
# apply convolution with circular disk B = D * B where D is disk kernel
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
cv2.filter2D(B, -1, disk, B)
B = np.uint8(B)
cv2.normalize(B, B, 0, 255, cv2.NORM_MINMAX)
# location of maximum intensity gives us location of object
    # if expecting region of image, thresholding gives nice result
ret, thresh = cv2.threshold(B, 50 255, 0)

# Backprojection in OpenCV
import cv2
import numpy as np

roi = cv2.imread('rose_red.png')
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

target = cv2.imread('rose.png')
hsvt = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)

# calculating the object histogram
roihist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

# normalize the histogram and apply Backprojection
cv2.normalize(roihist, roihist, 0, 255, cv2.NORM_MINMAX)
dst = cv2.calcBackProject([hsvt], [0, 1], roihist, [0, 180, 0, 256], 1)

# now convolute with circular disk
disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
cv2.filter2D(dst, -1, disk, dst)

# threshold and binary AND
ret, thresh = cv2.threshold(dst, 50, 255, 0)
thresh = cv2.merge((thresh, thresh, thresh))
res = cv2.bitwise_and(target, thresh)

res = np.vstack((target, thresh, res))
cv2.imwrite('res.jpg', res)
