import numpy as np
import cv2

img = cv2.imread('car2.png')

imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(imgHSV, np.array((0, 10, 10)), np.array((15, 255, 255)))
mask_cp = np.copy(mask)

im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

img = cv2.drawContours(img, contours, -1, (0, 255, 255), 3)
img2 = np.copy(img)
img3 = np.copy(img)
img4 = np.copy(img)
cnt = contours[0]
M = cv2.moments(cnt)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

cv2.circle(img2, (cx, cy), 5, (0, 255, 0), -1)
area = cv2.contourArea(cnt)
perimeter = cv2.arcLength(cnt, True)
hull = cv2.convexHull(cnt)

for i in hull:
    cv2.circle(img3, tuple(i[0]), 5, (255, 255, 255), -1)

x, y, w, h = cv2.boundingRect(cnt)
cv2.rectangle(img4, (x, y), (x+w, y+h), (255, 0, 255), 2)

cv2.imshow('mask', mask_cp)
cv2.imshow("contour", img)
cv2.imshow("centroid", img2)
cv2.imshow("hull", img3)
cv2.imshow("rectangle", img4)

cv2.waitKey(0)
cv2.destroyAllWindows
