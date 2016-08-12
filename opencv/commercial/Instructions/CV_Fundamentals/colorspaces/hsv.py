import cv2
import numpy as np

img = cv2.imread( "gorge.jpg" )
img_hsv = cv2.cvtColor( img, cv2.COLOR_BGR2HSV)

scale = .1 # numer 0-1

sat = img_hsv[..., 1]
maxSat = np.ones( sat.shape, dtype=np.uint8 )
augmentSat = np.uint8( scale * (255 - sat) )


# give an orange-ish hue
img_hsv[..., 0] = 15
img_hsv[..., 1] = sat + augmentSat
img_hsv[..., 1] = np.ones(img_hsv[..., 1].shape, dtype = np.uint8) * 30

img_new = cv2.cvtColor( img_hsv, cv2.COLOR_HSV2BGR )

cv2.imshow( "old", img )
cv2.imshow( "new", img_new )

cv2.waitKey(0)

cv2.destroyAllWindows()
