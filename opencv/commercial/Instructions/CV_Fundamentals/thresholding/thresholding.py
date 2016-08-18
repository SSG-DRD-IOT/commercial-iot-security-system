import cv2
import numpy as np

wake = cv2.imread( "wakeboard.jpg" )
whale = cv2.imread( "whale.jpg" )

gray = cv2.cvtColor( wake, cv2.COLOR_BGR2GRAY )
ret, mask = cv2.threshold( gray, 130, 255, cv2.THRESH_BINARY_INV ) # 119

# ROI
lu = (280, 170)
rb = (600, 490)
w = rb[0] - lu[0]
h = rb[1] - lu[1]

roi_mask = mask[ lu[1]:rb[1], lu[0]:rb[0] ]
roi_wake = wake[ lu[1]:rb[1], lu[0]:rb[0] ]
roi_wake = cv2.bitwise_and( roi_wake, roi_wake, mask=roi_mask )

# upper left corner of region in whale image where we will place wakeboarder
loc = (270, 60)
roi_whale = whale[ loc[1]:loc[1]+ h , loc[0]:loc[0] + w ]
roi_whale = cv2.bitwise_and( roi_whale, roi_whale, mask=cv2.bitwise_not(roi_mask) )
roi_whale = cv2.add( roi_whale, roi_wake )
whale[ loc[1] : loc[1]+ h , loc[0]:loc[0] + w ] = roi_whale

cv2.imshow("Internship 2016", whale)
cv2.waitKey(0)

cv2.destroyAllWindows()
