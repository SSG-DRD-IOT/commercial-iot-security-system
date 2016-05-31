"""
Otsu's binarization
uses parameter retVal

global thresholding -- uses arbitrary value for threshold (trial and error)
bimodal image (histogram has 2 peaks) - can approximately take value between the 2 peaks as threshold
- Otsu binarization - automatically calculates threshold value from image histogram for bimodal image
    automatically calculates threshold value from image histogram for bimodal image
function:
cv2.threshold(), pass extra flag: cv2.THRESH_OTSU
    --> for threshold value, PASS ZERO
    algorithm finds optimal threshold value, returns it as 2nd output
    (Otsu thresholding not used, retVal same as threshold value used)
"""

# example - imput image is noisy image.
#   1st case - global thresholding of 127
#   2nd case - Otsu's thresholding applied directly
#   3rd case - image filtered with 5x5 Gaussian kernel to remove noise, then Otsu thresholding applied
#       (noise filtering improves the result)

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('noisy2.png', 0)

# global thresholding
ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Otsu's thresholding
ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(img, (5,5), 0)
ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# plot all the images and their histograms
images =   [img, 0, th1,
            img, 0, th2,
            img, 0, th3]
titles = [  'Original Noisy Image',   'Histogram',   'Global Thresholding (v=127)',
            'Original Noisy Image',   'Histogram',   "Otsu's Thresholding",
            'Gaussian filtered Image','Histogram',   "Otsu's Thresholding"]
for i in xrange(3):
    plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
    plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
    plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
    plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
plt.show()

# SEE: Digital Image Processing, Rafael C. Gonzalez
