"""
Learn concepts of histogram equalization, use to improve contrast of images

If have image with pixel vals contained to specific range of vals only
    ex. brighter image having all pixels confined to high vals
    BUT good image has pixels from all regions of image
        -> need to stretch histogram to either ends
            ^what histogram equalization does
SEE: https://en.wikipedia.org/wiki/Histogram_equalization examples
    also check out https://www.youtube.com/watch?v=PD5d7EKYLcA
Essentially, if most values are clustered to a certain range, find cumulative
    probabily density and then multiply desired range by probabilities
"""

# Numpy implementation

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('wiki.jpg', 0)

hist, bins = np.histogram(img.flatten(), 256, [0, 256])

cdf = hist.cumsum()
cdf_normalized = cdf * hist.max() / cdf.max()

plt.plot(cdf_normalized, color = 'b')
plt.hist(img.flatten(), 256, [0, 256], color = 'r')
plt.xlim([0, 256])
plt.legend(('cdf', 'histogram'), loc = 'upper left')
plt.show()

# histogram lies in brighter region, but we need full spectrum
# need transformation function which maps input pixels in brighter region to input pixels in full region
    # -> histogram equalization
# now, find min histogram value, excluding 0, and apply histogram equalization eq'n
# use masked array concept from Numpy: for masked array, all ops performed on non-masked elements
cdf_m = np.ma.masked_equal(cdf, 0)
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
cdf = np.ma.filled(cdf_m, 0).astype('uint8')

# now, have look-up table giving us output pixel value for every input pixel value
    # just apply the transform
img2 = cdf[img]

# even if image darker one instead of brighter, after equalization get almost the same image we get here
# so this is a "reference tool" to make all images with same lighting conditions
    # useful for face recognition
    # images of faces histogram equalized to make them all with same lighting conditions

# Histogram Equalization in OpenCV
# opencv uses cv2.equalizeHist()
    # input: grayscale image
    # output: histogram equalized image

# code snippet:
img = cv2.imread('wiki.jpg', 0)
equ = cv2.equalizeHist(img)
res = np.hstack((img, equ)) # stacking images side by side
cv2.imwrite('res.png', res)

# Histogram equalization: good when histogram of img confined to a particular region
    # not good where theres large intensity variations where histogram covers large region: ie both bright and dark pixels present
