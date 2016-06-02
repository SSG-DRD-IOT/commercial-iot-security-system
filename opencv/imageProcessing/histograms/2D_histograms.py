"""
2D Histograms
find and plot

normally, used for finding color histograms where 2 features are hue and saturation values of each pixel

python sample samples/python/color_histogram.py already exists for finding color histograms
understand how to create such a color histogram; useful in understanding topics like Histogram Back-Projection
"""

# 2D Histogram in OpenCV
# calculated using same function, cv2.calcHist()
# color histograms: convert image from BGR -> HSV
    # (in 1D histogram, converted BGR to Grayscale)

# for 2D Histogram, modify parameters:
    # channels = [0, 1] b/c need to process both H and S plane
    # bins = [180, 256] 180 for H plane and 256 for S plane
    # range = [0, 180, 0, 256] hue value lies between 0 and 180; saturation between 0 and 256

import cv2
import numpy as np

img = cv2.imread('home.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

# 2D Histogram in Numpy
# numpy provides function np.histogram2d() (for 1D histogram use np.histogram())
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('home.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hist, xbins, ybins = np.histogram2d(h.ravel(), s.ravel(), [180, 256], [[0, 180], [0, 256]])
# 1st arg is H plane, 2nd is S plane, 3rd is # of bins for each, 4th is their range

# Plotting 2D Histograms
# method1: use cv2.imshow()
    # result is 2D array of size 180x256; can show as we do normally with cv2.imshow() function
    # will be grayscale image and won't give much idea what colors are there
# method2: use matplotlib
    # use matplotlib.pyplot.imshow() function to plot 2D histogram with different color maps
    # gives us better idea about different pixel density
    # REMEMBER: using this, interpolation flag should be nearest for better results
import cv2
import numpy as np
from matplotlib impot pyplot as plt

img = cv2.imread('home.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hist = cv2.calcHist( [hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

plt.imshow(hist, interpolation='nearest')
plt.show()

# method3: OpenCV Sample Style
    # run code from OpenCV-Python2 samples, see histogram also shows corresponding color
        # or simply outputs a color coded histogram
