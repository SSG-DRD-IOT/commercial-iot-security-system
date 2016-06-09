import cv2
import numpy as np

moon = cv2.imread('moon.jpg')

# kernel = np.ones((8,8), np.float32)/64
# moon = cv2.filter2D(moon, -1, kernel)
# moon = cv2.GaussianBlur(moon, (15,15), 5)
moon = cv2.bilateralFilter(moon, 100, 80, 150)
# cv2.imshow('moon', moon)
cv2.imwrite('moon_fixed.jpg', moon)
cv2.waitKey(0)
cv2.destroyAllWindows()
