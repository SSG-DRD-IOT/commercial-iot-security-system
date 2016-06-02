"""
Interactive Foreground Extraction using GrabCut Algorithm
- use GrabCut to extract foreground in images
- create an interactive application

GrabCut - algorithm for foreground extraction with minimal user interaction

from user POV:
    initially, user draws rectangle around foreground region
        foreground region completely inside the rectangle
    algorithm then segments it iteratively to get best result
    sometimes, segmentation not fine - ie fg and bg regions mixed in markings
        give some strokes on images where there are faulty results
            next interation, get better results
ex. enclose player and football in blue rectangle, add some final touchups with:
    white strokes - denote foreground
    black strokes - denote background

what happens "behind the scenes":

-) user inputs rectangle; everything outside rectangle taken as sure background
    why rectangle should include all objects
    everything inside rectangle is unknown
    any user input specifying fg/bg are considered hard-labelling
        won't change in the process
-) computer does initial labeling depending on given data
    labels foreground and background pixels (hard-labels)
-) a Gaussian Mixture Model (GMM) is used to model fg & bg
-) based on date we give, GMM learns & creates new pixel distribution
    unknown pixels labeled either probable fg or probable bg, depending on rel'n w/ other hard-labeled pixels in terms of color statistics
        like clustering
-) graph is build from pixel distribution
    nodes in graph are pixels
        additional 2 nodes added: source node and sink node
    every foreground pixel connected to source node, every bg pixel to sink node
-) weights of edges connecting pixels to source node/end node defined by probability of pixel being fg/bg
    weights between pixels defined by edge information or pixel similarity
    if theres a large diff in pixel color, edge between them gets low weight
-) mincut algorithm segments graph
    cuts graph into 2 separate source node and source sink with minimum cost function
    cost function is sum of all weights of the edges that are cut
    after cut, all pixels connected to source node become foreground, those connected to sink node become bg
-) process is continued until classification converges
"""

# GrabCut in OpenCV
# function: cv2.grabCut()
# arguments:
    # img - input image
    # mask - mask image where we specify which areas are bg, fg, or probable bg/fg, ...
        # done with flags: cv2.GC_BGD, cv2.GC_FGD, cv2.GC_PR_BGD, cv2.GC_PR_FGD, or simply pass 0, 1, 2, 3
    # rect - coords of a rectangle which includes fg object in the format (x, y, w, h)
    # bgdModel, fgdModel - arrays used  by algorithm internally. Create two np.float64 type zero arrays of size (1,65)
    # iterCount - number of iterations the algorithm should run
    # mode - should be cv2.GC_INIT_WITH_RECT or cv2.GC_INIT_WITH_MASK or combined, which decides whether we're drawing
    #   rectangle or final touchup strokes

# ex. rectangular mode
import numpy as np
import cv2
from matplotlib import pyplot as plt

# load the image
img = cv2.imread('messi5.jpg')
# create similar image mask
mask = np.zeros(img.shape[:2], np.uint8)

# create fgdModel and bgdModel
bgdModel = np.zeros((1,65), np.float64)
fgdModel = np.zeros((1,65), np.float64)

# give rectangle parameters
rect = (50, 50, 450, 290)
# algorithm runs 5 iterations, mode is rectangle so cv2.GC_INIT_WITH_RECT
cv2.grabcut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
# run grabcut - modifies mask image

# in new mask image, pixels marked with 4 flags denoting bg/fg as specified above
mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
img = img*mask2[:, :, np.newaxis]
# modify mask st all 0-pixels and 2-pxls are put to 0 (ie bg) and all 1- and 3-pixels put to 1 (is foreground pixels)
# now, final mask ready - just multiply with input image to get segmented image
plt.imshow(img), plt.colorbar(), plt.show()

# problem: hair is gone, want it - give fine touchup with 1-pixel(sure foreground)
# part of ground and logo are in picture - need to be removed
    # give 0-pixel touchup (sure bg)
    # open input image in paint, add another layer to image
        # using brush tool, mark missed fg with white, unwanted bg in black on new layer
        # fill rem bg with gray
        # load masked img in OpenCV, edit original mask img we got with corresp values in newly added mask image

# newmask is the mask image I manually labeled
newmask = cv2.imread('newmask.png', 0)

# whereever it is marked white (sure fg), change mask = 1
# whereever it is marked black (sure bg), change mask = 0
mask[newmask == 0] = 0
mask[newmask == 255] = 1

mask, bgdModel, fgdModel = cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

mask = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
img = img*mask[:,:,np.newaxis]
plt.imshow(img), plt.colorbar(), plt.show()

# instead of initializing in rect mode, can go directly into mask mode
    # mark rectangle area in mask image with 2-pixel or 3-pixel (probable bg/fg)
    # mark sure_foreground with 1-pixel, as in 2nd example
    # apply grabCut function with mask mode
