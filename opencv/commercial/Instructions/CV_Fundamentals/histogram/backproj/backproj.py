
import cv2
import numpy as np

roi = cv2.imread( 'mtn1.jpg' )
hsv = cv2.cvtColor( roi, cv2.COLOR_BGR2HSV )

target = cv2.imread( 'mtn2.jpg' )
hsvt = cv2.cvtColor( target, cv2.COLOR_BGR2HSV )

mask = np.zeros( roi.shape[0:2], np.uint8 )
mask[302:1000, 766:1617] = 255

# calculating the object histogram
roihist = cv2.calcHist( [hsv], [0, 1], mask, [180, 256], [0, 180, 0, 256] )
cv2.imwrite("hist.jpg", roihist)

# normalize the histogram and apply Backprojection
cv2.normalize( roihist, roihist, 0, 255, cv2.NORM_MINMAX )
prob = cv2.calcBackProject( [hsvt], [0, 1], roihist, [0, 180, 0, 256], 1 )

# # now convolve with circular disk
disk = cv2.getStructuringElement( cv2.MORPH_ELLIPSE, ( 5,5 ) )
prob = cv2.filter2D( prob, -1, disk)

cv2.imshow( 'probability', prob )
cv2.imshow("hist", roihist)

# cv2.imwrite( 'probability.jpg', prob )

cv2.waitKey( 0 )

cv2.destroyAllWindows(  )
