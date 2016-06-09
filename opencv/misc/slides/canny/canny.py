import cv2
import numpy as np

wreck = cv2.imread('wreck.jpg', 0)
a = 4
b = 4
kernel = np.ones((a,b), np.float32)/(a*b)
wreck = cv2.filter2D(wreck, -1, kernel)
# moon = cv2.GaussianBlur(wreck, (15,15), 5)
# moon = cv2.bilateralFilter(wreck, 30, 10, 10)
edges = cv2.Canny(wreck, 0, 200)
cv2.imshow('wreck', wreck)
cv2.imshow('canny', edges)
cv2.imwrite('canny.jpg', edges)
cv2.imwrite('wreckBlurred.jpg', wreck)
cv2.waitKey(0)
cv2.destroyAllWindows()
