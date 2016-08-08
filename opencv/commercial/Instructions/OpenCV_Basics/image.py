import cv2
img = cv2.imread( 'image.jpg' )
cv2.imshow( "Image", img )
cv2.waitKey( 0 )
cv2.imwrite( "new_image.jpg", img )
cv2.destroyAllWindows()
