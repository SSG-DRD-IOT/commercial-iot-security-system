import numpy as np
import cv2

img = cv2.imread('car.jpg')

imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#  Hue is in <value> % 180
mask_r1 = cv2.inRange(imgHSV, np.array((0, 100, 5)), np.array((10, 255, 230))) # reds above 0
mask_r2 = cv2.inRange(imgHSV, np.array((161, 100, 20)), np.array((179, 255, 200))) # reds below 0
mask = cv2.bitwise_or(mask_r1, mask_r2)

imgHSV[ ..., 0 ] = 120
imgHSV[ ..., 1 ] = 255

imgBlue = cv2.cvtColor(imgHSV, cv2.COLOR_HSV2BGR)
imgNew_car = cv2.bitwise_and(imgBlue, imgBlue, mask=mask)
imgNew_nocar = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask))

imgNew = cv2.add(imgNew_car, imgNew_nocar)

cv2.imshow("new", imgNew)

cv2.waitKey(0)
cv2.destroyAllWindows
