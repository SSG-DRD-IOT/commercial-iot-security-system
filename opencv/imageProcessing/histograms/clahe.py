"""
CLAHE (Contrast Limited Adaptive Histogram Equlization)

First histogram equalization considers global contrast of image: sometimes, not a good idea

ex. if bright face and dark background, after equalization BG improves but face becomes too bright and features difficult to distinguish

Solution: Adaptive Histogram Equalization
    image divided into small blocks called "tiles" (tileSize=8x8 by default in OpenCV)
    Each block histogram equalized as usual
    -> in small area, histogram confined to a small region, unless there's noise
        if noise, it's amplified (bad)
    contrast limiting applied to remove noise
        if any histogram bin above specified contrast limit (default 40), pixels are clipped and distributed uniformly to other bins before applying H.Eq.
    After equalization, to remove artifacts in tile borders, bilinear interpolation applied
"""

# CLAHE in OpenCV:

import numpy as np
import cv2

img = cv2.imread('tsukuba_l.png', 0)

# create a CLAHE object (Arguments are optional)
clahe = cv2.createCLAHE(clipLimit=2.0,  tileGridSize=(8,8))
cl1 = clahe.apply(img)

cv2.imwrite('clahe_2.jpg', cl1)
