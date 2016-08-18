import cv2
import numpy as np

img = cv2.imread( "street.jpg" )

blur = cv2.blur( img, (9,9) )
gauss = cv2.GaussianBlur( img, (9,9), 3 )
median = cv2.medianBlur(img, 9)

cv2.imshow("Mean", blur)
cv2.imshow("Gaussian", gauss)
cv2.imshow("Median", median)

cv2.imwrite("mean.jpg", blur)
cv2.imwrite("gaussian.jpg", gauss)
cv2.imwrite("median.jpg", median)

cv2.waitKey(0)
cv2.destroyAllWindows()
