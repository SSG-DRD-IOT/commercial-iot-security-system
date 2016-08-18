
import cv2
import numpy as np

img = cv2.imread('whale.jpg', 0)
# img = cv2.GaussianBlur(img, (5,5), 21)
# img = cv2.medianBlur(img, 11)


#
# sobel_x = cv2.Sobel(img, 0, 1, 0, ksize=1)
# sobel_y = cv2.Sobel(img, 0, 0, 1, ksize=1)
#

sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
laplacian = cv2.Laplacian(img, 0)

sobel_x = np.absolute( sobel_x )
sobel_y = np.absolute( sobel_y )
sobel_x = np.uint8( sobel_x )
sobel_y = np.uint8( sobel_y )

# laplacian = cv2.Laplacian(img, cv2.CV_64F)
# print np.max(laplacian)
# laplacian = np.absolute(laplacian)
# laplacian = 255 * laplacian / np.max(laplacian)
# laplacian = np.uint8(laplacian)
cv2.imshow( "Sobel x", sobel_x )
cv2.imshow( "Sobel y", sobel_y )
cv2.imshow( "laplacian", laplacian )
cv2.imshow( "image", img )

cv2.imwrite( "sobelx.jpg", sobel_x )
cv2.imwrite( "sobely.jpg", sobel_y )
cv2.imwrite( "laplacian.jpg", laplacian )
cv2.imwrite( "imageGray.jpg", img )

cv2.waitKey(0)
cv2.destroyAllWindows()
