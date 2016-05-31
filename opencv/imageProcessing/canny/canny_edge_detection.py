"""
Canny Edge Detection
function:
cv2.Canny()
"""
# Popular edge detection algorithm
    # multi-stage algorithm
    # noise reduction
        # first step is to remove noise from image w/ 5x5 Gaussian filter
    # finding intensity gradient of image
        # smoothed image filtered with Sobel kernel in both horiz and vert direction to get 1st deriv in horiz direction (G_x)
        # and vertical dir (G_y) then find edge gradient and direction for each pixel as follows:
        # Edge_Gradient G=sqrt(G_x^2 + G_y^2)
        # Angle (/theta) = atan(G_y/G_x)
        # gradient direction always perpendicular to edges
            # rounded to one of 4 angles representing vertical, horiz, and 2 diag directions
    # Non-maximum Suppression
        # after getting gradient mag and dir, full scan removes any unwanted pixels not constituting an edge
            # at every pixel, pixel is checked if it is local max in its nbhd in dir of gradient
                # if so, moves on to next stage; otw is suppressed
        # result is a binary image with "thin edges"
    # Hysteresis Thresholding
        # decides which are real edges and which are not
        # need 2 threshold values, minVal and maxVal
        # any edges with intensity gradient > maxVal sure to be edges, those below minVal sure to be non-edges so discarded
        # those between thresholds classified based on connectivity
            # if connected to "sure-edge" pixels part of edges, otw discarded
        # so must select minVal and maxVal accordingy
        # removes small pixels noises; assumes that edges are long lines
    # --> strong edges in image

# Canny Edge Detection in OpenCV
# all in single function, cv2.Canny()
    # arguments: input image, minVal, maxVal, aperture_size - size of Sobel kernel used to find image gradients; 3 by default, L2gradient, specifying eq'n for finding gradient maginitude
        # True --> uses eq'n above, more accurate; otherwise, uses Edge_Gradient (G) = |G_x|+|G_y| (False by default)
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('messi5.jpg', 0)
edges = cv2.Canny(img, 100, 200)

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(edges, cmap='gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
