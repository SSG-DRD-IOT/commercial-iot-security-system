"""
access pixel values and modify them
access image properties
setting the Region of Image (ROI)
splitting and merging images

all of these are more Numpy than OpenCV
"""

# NOTE: codes meant to run in Python terminal, for single lines of code

# load color image
import cv2
import numpy as np

img = cv2.imread('messi5.jpg')

# -----
# Access and modify pixel values
# -----

# access pixel value by row and col coords; for BGR, returns array of blue, green, red values
# grayscale -- just corresponding intensity returned
px = img[100,100]
print px

# accessing only blue pixel
blue = img[100,100,0]
print blue

# can modify pixel val same way
img[100,100] = [255,255,255]
print img[100,100]

# WARNING: numpy optimized for fast array calculationsl simply accessing each pixel value
# and modifying it is very slow

# NOTE: above method used for selecting region of array [first M rows and N cols]
# for individual pixel access, array methods array.item() and array.itemset() better (but always return a scalar)
# ie to access all BGR vals, need to call array.item() separately

# accessing RED value
img.item(10,10,2)

# modifying RED value
img.itemset((10,10,2), 100)
print img.item(10,10,2)

# -----
# Access image properties
# -----
# image properties include # of rows, cols and channels, type of img data, # pixels, ...
print img.shape

# image is grayscale - returned tuple contains only # of rows and cols ( good check to see if grayscale)

# total # pixels accessed with img.size
print img.size

# image datatype obtained with img.dtype
print img.dtype
# NOTE: important, for many errors caused by invalid datatype

# -----
# Image ROI
# -----

# sometimes, play with certain regions of images
# use Numpy indexing

# select ball, cpy to another region of image
ball = img[280:340, 330:390]
img[273:333, 100:160] = ball
# cv2.imshow('image', img)
# cv2.waitKey(0)

# -----
# Splitting and Merging Image channels
# -----

# can split BGR images to single planes or join indiv channels to BGR image
b, g, r = cv2.split(img)
img = cv2.merge((b, g, r))

# or
b = img[:,:,0]

# ex. to make all red pixels zero, use Numpy indexing
img[:,:,2] = 0

# cv2.split() is costly operation in terms of time, so only use if needed; Numpy indexing otw


cv2.imshow('image', img)
cv2.waitKey(0)
