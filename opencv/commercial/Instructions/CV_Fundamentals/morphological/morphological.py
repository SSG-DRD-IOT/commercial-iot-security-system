import cv2
import numpy as np
img = cv2.imread( 'euler.jpg', 0 )

_, img = cv2.threshold( img, 30, 255, cv2.THRESH_BINARY )
kernel = cv2.getStructuringElement( cv2.MORPH_ELLIPSE, ( 2,2 ) )

img = cv2.morphologyEx( img, cv2.MORPH_OPEN, kernel )
# cv2.imwrite( 'opened.jpg', img )

img = cv2.erode( img, kernel )
cv2.imshow( 'img', img )
# cv2.imwrite( 'combo.jpg', img )
cv2.waitKey( 0 )
cv2.destroyAllWindows(  )
