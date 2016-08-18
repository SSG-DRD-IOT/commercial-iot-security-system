import cv2
from matplotlib import pyplot as plt

img = cv2.imread('winter.jpg', 0)
equ = cv2.equalizeHist(img)

hist = cv2.calcHist([img], [0], None, [256], [0, 256])
histEq = cv2.calcHist([equ], [0], None, [256], [0, 256])

plt.figure(1)
plt.plot(hist)
plt.xlim([0, 256])

plt.figure(2)
plt.plot(histEq)
plt.xlim([0, 256])

cv2.imshow("image", img)
cv2.imshow("eq", equ)
cv2.imshow("image", img)
cv2.imshow("eq", equ)
plt.show()
cv2.waitKey(0)
cv2.imwrite("equalized.jpg", equ)
cv2.destroyAllWindows
plt.close('all')
