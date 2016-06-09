
import cv2
import numpy as np

roi = cv2.imread('mtn1.jpg')
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

target = cv2.imread('mtn2_lo.jpg')
hsvt = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)

mask = np.zeros(np.shape(roi), np.uint8)
mask[302:1000, 766:1617] = 255 #766 302, 1617, 1000

# calculating the object histogram
roihist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

# normalize the histogram and apply Backprojection
cv2.normalize(roihist, roihist, 0, 255, cv2.NORM_MINMAX)
# cv2.imshow('roihist' ,roihist)
dst = cv2.calcBackProject([hsvt], [0, 1], roihist, [0, 180, 0, 256], 1)

# # now convolute with circular disk
disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
cv2.filter2D(dst, -1, disk, dst)
#
# # threshold and binary AND
# ret, thresh = cv2.threshold(dst, 50, 255, 0)
# thresh = cv2.merge((thresh, thresh, thresh))
# res = cv2.bitwise_and(target, thresh)
# cv2.imshow('dist', dst)
cv2.imwrite('dst.jpg', dst)
cv2.imwrite('hist.jpg', roihist)
# res = np.vstack((target, thresh, res))
# cv2.imwrite('res.jpg', res)
