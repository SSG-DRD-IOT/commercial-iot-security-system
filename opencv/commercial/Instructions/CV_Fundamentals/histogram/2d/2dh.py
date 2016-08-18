import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('mountain.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# cv2.imshow('hsv', hsv)
hist = cv2.calcHist( [hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
print hist
hist = cv2.applyColorMap(hist, cv2.COLORMAP_HSV)
# cv2.imshow('histogram', hist)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
cv2.imwrite('hist.jpg', hist)
# plt.imshow(hist,interpolation = 'nearest')
# plt.show()
