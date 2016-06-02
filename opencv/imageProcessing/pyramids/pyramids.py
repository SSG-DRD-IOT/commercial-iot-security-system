"""
Image Pyramids
functions: cv2.pyrUp(), cv2.pyrDown()

sometimes, need to work with images of different resolution of the same image
    create images with different resolution, search for object in all the images
image pyramid = {images of different resolution}
pyramid types
    Gaussian pyramid
    Laplacian pyramid
"""

# Higher level(Low resolution) in Gaussian
    # remove consecutive rows and cols in lower level (higher res) image
        # each pixel in higher level formed by contribution from 5 pixels in underlying lower level with Gaussian weights
        # thus, MxN image becomes M/2 x N/2 image
        # so area reduced by 1/4 of original area -- called an Octave
        # expanding, area becomes 4x in each level
    # Gaussian pyramids: cv2.pyrDown() and cv2.pyrUp()
img = cv2.imread('messi5.jpg')
lower_reso = cv2.pyrDown(higher_reso)

# go down image pyramid with cv2.pyrUp() function
higher_reso2 = cv2.pyrUp(lower_reso)

# NOTE: higher_reso2 != higher_reso, for when you decrease the resolution, you loose the information

# Laplacian Pyramids
    # formed from Gaussian pyramids
    # Laplacian pyr edges are edge images only
        # mose elements are zeros
        # used in image compression
    # level is formed by diff btwn lvl in Gaussian pyramid and expanded version of its upper level in Gaussian pyramid

# Image Blending using Pyramids

# in image stitching, need to stack 2 images together; amy not look good due to image discontinuities
# image blending gives seamless blending without leaving much data

# ex. blend apple and orange
    # load apple and orange images
    # find Gaussian pyramids for apple and orange
    # from G.pyramids, find Laplacian pyramids
    # join left hald of apple and right hald of orange in each levels of Laplacian pyramids
    # from joint image pyramids, reconstruct original image

import cv2
import numpy as np, sys

A = cv2.imread('apple.jpg')
B = v2.imread('orange.jpg')

# generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in xrange(6):
    G = cv2.pyrDown(G)
    gpA.append(G)

# generate Gaussian pyramid for B
G = B.copy()
gpB = [G]
for i in xrange(6):
    G = cv2.pyrDown(G)
    gpB.append(G)

# generate Laplacian pyramid for A
lpA = [gpA[5]]
for i in xrange(5,0,-1):
    GE = cv2.pyrUp(gpA[i])
    L = cv2.subtract(gpA[i-1], GE)
    lpA.append(L)

# generate Laplacian pyramid for B
lpB = [gpB[5]]
for i in xrange(5,0,-1):
    GE = cv2.pyrUp(gpB[i])
    L = cv2.subtract(gpB[i-1], GE)
    lpB.append(L)

# Add left and right halves of images in each level
LS = []
for la, lb in zip(lpA, lpB):
    rows, cols, dpt = la.shape
    ls = np.hstack((la[:, 0:cols/2], lb[:, cols/2:]))
    LS.append(ls)

# now reconstruct
ls_ = LS[0]
for i in xrange(1,6):
    ls_ = cv2.pyrUp(ls_)
    ls_ = cv2.add(ls_, LS[i])

# image with direct connecting each half
real = np.hstack((A[:,:cols/2], B[:, cols/2:]))

cv2.imwrite('Pyramid_blending2.jpg', ls_)
cv2.imwrite('Direct_blending.jpg', real)
