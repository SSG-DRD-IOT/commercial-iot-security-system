import cv2
import numpy as np
img = np.zeros( ( 480, 640, 3 ), np.uint8 )

cv2.line( img, (0, 0), (639, 479), (255, 255, 255), 3 )

points = np.array( [ (5, 10), (20, 400), (55, 400), (400, 20) ], np.int32 )
points = points.reshape( ( -1, 1, 2 ) )
cv2.polylines( img, [points], True, ( 0, 255, 0 ) )

cv2.rectangle( img, (40, 10), (230, 300), (0, 255, 255), 2 )

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText( img, 'Hello Worlds!', (200, 460), font, 2, (255, 255, 0), 2, cv2.LINE_AA )

cv2.imshow( 'My Drawing', img )
cv2.waitKey(0)
