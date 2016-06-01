"""
use marker-based segmentation with watershed algorithm
function: cv2.watershed()

view any grayscale img as topographic surface
    high intensity - peaks
    low intensity - valleys
start: fill every local minima with labels
depending on peaks(gradients) nearby, labels start to merge
    avoid by building barriers at merges
continue filling until all peaks are "underwater"
    then, barriers give segmentation result
    SEE: http://cmm.ensmp.fr/~beucher/wtshed.html
^ approach gives oversegmented result due to noise or irregularities in image
OpenCV: marker-based watershed algorithm
    specifyw chich arel all merged and all not merged valley pts
        an interactive image segmentation
    give different labels to object we know
    -> label region we are sure of being foreground with one color/intensity
        label region we are sure of being background/non-object with another color
        label region which we are unsure of with 0
        ^ this is our marker
    apply watershed algorithm
    then, our marker updated with the labels we give, and boundaries of objects have a value of -1
"""

# Distance Transform along with Watershed to segment mutually touching objects

# ex. coins touching in image; even with thresholding, they still touch

# start with finding approximate estimate of the coins: use Otsu's binarization
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('coins.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# now, remove small white noises in the image
    # use morphological opening
# remove small holes in object
    # use morphological closing
# now know region near center of objects foreground, region away from object is background
# only not sure about boundary region of coins

# extract area where we're sure there are coins
    # erosion removes boundary pixels
    # whatever remains, we can be sure it's a coin
    # would work if objects not touching each other
# touching e/o -> good to find distance transform & apply proper threshold
# next, find area where sure there aren't coins
    # dilate result
        # increase object boundary to bg
    # can compute whatever region in bg in result really a background, since boundary region is removed
# remaining regions: we don't have any idea, whether it's coins or background
    # find using Watershed algorithm
# areas normally around boundaries of coins where foreground and bg meet or 2 coins meet
    # called "border"
# obtain by subtracting sure_fg and sure_bg areas

# noise removal
kernel = np.ones((3,3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening, kernel, iterations = 3)

# finding sure foreground area
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)

# finding the unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)
# in thresholded image, get some regions of coins which we're sure are cins and which are detached now
# sometimes, may only be interested in foreground segmentation, NOT in separating mutually touching objects
    # then, do not need distance transform, just erosion sufficient
# erosion = just another method to extract sure fg area

# now, know for sure which are regions of coins, which are background
# want to create marker (array of same size as orig img, but with int32 datatype), label inside regions
# regions known for sure, whether fg or bg, labeled with any positive ints, img with 0, other objects labeled with integers starting with 1
# know: if bg marked with 0, watershed considers it as unknown area
    # so mark with different int
# instead, mark unknown region, defined as unknown, with 0

# marker labeling
ret, markers = cv2.connectedComponents(sure_fg)

# add one to all labels so that sure background is not 0 but 1
markers = markers + 1

# now, mark region of unknown with 0
markers[unknown == 255] = 0

# markers ready; finally, apply watershed
# marker image will be modified
    # boundary region marked with -1
markers = cv2.watershed(img, markers)
img[markers == -1] = [255, 0, 0]
