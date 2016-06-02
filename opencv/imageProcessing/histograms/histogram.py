"""
Histograms
Find, Plot, Analyze
    finding histograms using OpenCV and Numpy
    plotting histograms using OpenCV and Matplotlib
functions:
cv2.calcHist()
np.histogram()

histogram - plot giving overall intensity distribution of image
    plot w/ pixel vals in X-axis and corresponding pixels in image on Y-axis
"""

# Finding histogram
# terminology:
    # BINS - split the histogram into subparts, where each subpart is called a BIN.
        # represented by term histSize in OpenCV
    # DIMS - number of parameters for which we collect the data
        # ex. if only for intensity value, then 1
    # RANGE - range of intensity values you measure; normally, [0, 256] ie all intensity values

# Histogram calculation in OpenCV
# use cv2.calcHist() function to find histogram
    # cv2.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])
    # parameters:
        # images - source image of type uint8 or float32; given in square brackets, ie [img]
        # channels - also in sq brackets; index of channel for which we calculate histogram
            # ex. if grayscale img, value is [0]; for color image, can pass [0], [1], or [1] to calc B, G, or R channel
        # mask - mask image; to find hist of full image, give as "None"
            # if want to find hist of particular regin of image, cr. a mask image for that and give as mask
        # histSize - represents BIN count; give in square brackets. Full scale: pass [256]
        # ranges - our RANGE; normally, [0, 256]
# example: load image in grayscale mode, find its full histogram
img = cv2.imread('home.jpg', 0)
hist = cv2.calcHist([img], [0], None, [256], [0, 256]) # hist is 256x1 array; each val corresponds to # of pixels in that image w/ corresponding pixel value

# Histogram calculation in Numpy
# numpy provides np.histogram()
hist, bins = np.histogram(img.ravel(), 256, [0, 256])
# bins has 257 elements, b/c numpy calculates bins as 0-0.99, 1-2.99, 2-2.99, etc.
    # final range 255-255.99, ao also add 256 to end of bins; up to 255 is sufficient
# SEE: np.bincount() much faster than np.histogram; use for 1-dim'l histograms
    # set minlength=256 in np.bincount ex. hist=np.bincount(img.ravel(), minlength=256)
# NOTE: OpenCV much faster than np.histogram()

# plotting using Matplotlib
# histogram plotting function: matplotlib.pyplot.hist()
# directly finds and plots histogram; calcHist() or np.histogram() unnecessary
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('home.jpg', 0)
plt.hist(img.ravel(), 256, [0, 256]); plt.show()

# use normal plot of matplotlib, good for BGR plot; need to find histogram data first
import cv2
import numpy as np

img = cv2.imread('home.jpg')
color = ( 'b', 'g', 'r' )
for i, col in enumerate(color):
    histr = cv2.calcHist([img], [i], None, [256], [0, 256])
    plt.plot(histr, color = col)
    plt.xlim([0, 256])
plt.show()

# Using OpenCV
# can use vals of histograms along with bin vals to look like x, y coords to generate graph with cv2.line() or cv2.polyline() function

# Mask application
# use calcHist to find histogram of full image
# to find histograms of regions of an image, create mask image w/ white color on region wanted, black otherwise; then, pass the mask

img = cv2.imread('home.jpg', 0)
# create a mask
mask = np.zeros(img.shape[:2], np.uint8)
mask[100:300, 100:400] = 255
masked_img = cv2.bitwise_and(img, img, mask=mask)

# calculate histogram with mask and without mask
# check 3rd argument for mask
hist_full = cv2.calcHist([img], [0], None, [256], [0, 256])
hist_mask = cv2.calcHist([img], [0], mask, [256], [0, 256])

plt.subplot(221), plt.imshow(img, 'gray')
plt.subplot(222), plt.imshow(mask, 'gray')
plt.subplot(223), plt.imshow(masked_img, 'gray')
plt.subplot(224), plt.plot(hist_full), plt.plot(hist_mask)
plt.xlim([0, 256])

plt.show()

# SEE: Cambridge in Color
