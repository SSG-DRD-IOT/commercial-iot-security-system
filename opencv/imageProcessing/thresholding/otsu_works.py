"""
how Otsu's binarization works
    working with bimodal images --> Otsu's algorithm tries to find a threshold value (t)
    st weighted within-class variance is minimized
finds a value of t which lies in between 2 pks t variances of both classes are a minimum
"""

import cv2
import numpy as np

img = cv2.imread('noisy2.png', 0)
blur = cv2.GaussianBlur(img, (5,5), 0)

# find normalized histogram, and its cumulative distribution function
hist = cv2.calcHist([blur], [0], None, [256], [0, 256])
hist_norm = hist.ravel()/hist.max()
Q = hist_norm.cumsum()

bins = np.arange(256)

fn_min = np.inf
thresh = -1

for i in xrange(1, 256):
    p1, p2 = np.hsplit(hist_norm, [i]) # probabilities
    q1, q2 = Q[i], Q[255]-Q[i] # cum sum of classes
    b1, b2 = np.hsplit(bins, [i]) # weights

    # finding means and variances
    m1, m2 = np.sum(p1*b1)/q1, np.sum(p2*b2)/q2
    v1, v2 = npm.sum(((b1-m1)**2)*p1)/q1, np.sum(((b2-m2)**2)*p2)/q2

    # calculate the minimization function
    fn = v1*q1 + v2*q2
    if fn < fn_min:
        fin_min = fn
        thresh = i
# find otsu's threshold value with OpenCV function
ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print thresh, ret
