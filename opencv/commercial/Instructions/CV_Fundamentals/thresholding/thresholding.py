# wake whale
import cv2
import numpy as np

wake = cv2.imread("wakeboard.jpg")
whale = cv2.imread("whale.jpg")
gray = cv2.cvtColor(wake, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY_INV) # 119
mask_inv = cv2.bitwise_not(mask)

loc = (270, 60)

# ROI
lu = (280, 170)
rb = (600, 490)
w = rb[0] - lu[0]
h = rb[1] - lu[1]

roi_mask = mask[lu[1]:rb[1], lu[0]:rb[0]]
roi_mask_inv = mask_inv[lu[1]:rb[1], lu[0]:rb[0]]

roi_wake = wake[lu[1]:rb[1], lu[0]:rb[0]]
roi_wake = cv2.bitwise_and(roi_wake, roi_wake, mask=roi_mask)
wkCpy = np.copy(roi_wake)
roi_whale = whale[ loc[1]:loc[1]+ h , loc[0]:loc[0] + w  ]
roi_whale = cv2.bitwise_and(roi_whale, roi_whale, mask=roi_mask_inv)
wlCpy = np.copy(roi_whale)
roi_whale = cv2.add(roi_whale, roi_wake)
whale[ loc[1]:loc[1]+ h , loc[0]:loc[0] + w  ] = roi_whale

cv2.imwrite("roi whale.jpg", roi_whale)
cv2.imwrite( "whaleNew.jpg", whale)
cv2.imwrite("wakewhale.jpg", whale)
cv2.imwrite("roi mask.jpg", roi_mask)
cv2.imwrite("roi mask_inv.jpg", roi_mask_inv)
cv2.imwrite("mask.jpg", mask)
cv2.imwrite("mask_inv.jpg", mask_inv)
cv2.imwrite("wkCpy.jpg", wkCpy)
cv2.imwrite("wlCpy.jpg", wlCpy)

# cv2.imshow("roi whale.jpg", roi_whale)
# cv2.imshow( "whaleNew.jpg", whale)
# cv2.imshow("wakewhale.jpg", whale)
# cv2.imshow("roi mask.jpg", roi_mask)
# cv2.imshow("roi mask_inv.jpg", roi_mask_inv)
# cv2.imshow("mask.jpg", mask)
# cv2.imshow("mask_inv.jpg", mask_inv)
# cv2.imshow("wkCpy.jpg", wkCpy)
# cv2.imshow("wlCpy.jpg", wlCpy)


cv2.waitKey(0)

cv2.destroyAllWindows()
# plt.close('all')
