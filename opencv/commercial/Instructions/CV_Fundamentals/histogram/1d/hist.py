import cv2
from matplotlib import pyplot as plt

img = cv2.imread( 'winter.jpg', 0 )

hist = cv2.calcHist( [img], [0], None, [256], [0, 256] )

cv2.imwrite( "winter_gray.jpg", img )
plt.plot( hist )
plt.xlim( [0, 256] )
plt.show(  )
