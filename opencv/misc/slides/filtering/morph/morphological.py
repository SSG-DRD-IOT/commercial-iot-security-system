import cv2
import numpy as np
img = cv2.imread('eulerBNoise.jpg', 0)
# img = (255 * np.ones(np.shape(img), np.uint8)) - img
# cv2.imshow('imgt', img)
# imD =
# cv2.imwrite('eulerB.jpg', img)

_, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
img = cv2.erode(img, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=2)
img = cv2.erode(img, kernel, iterations=1)

# ---------
# img = cv2.erode(img, kernel, iterations=1)
# img = cv2.dilate(img, kernel, iterations=2)
# img = cv2.erode(img, kernel, iterations=2)
# img = cv2.dilate(img, kernel, iterations=2)
# _, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
# img = cv2.dilate(img, kernel, iterations=3)
# img = cv2.erode(img, kernel, iterations=2)
cv2.imshow('img', img)
cv2.imwrite('combo.jpg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
