import cv2
import numpy as np

clock = cv2.imread( 'clock.jpg', 0 )

clock = cv2.GaussianBlur( clock, (3, 5), 0.525, .9)
edges = cv2.Canny( clock, 53, 160 )
cv2.imshow( 'clock', clock )
cv2.imshow( 'canny', edges )

# cv2.imwrite("clock_gaussgray.jpg", clock)
# cv2.imwrite("edges.jpg", edges)

cv2.waitKey( 0 )
cv2.destroyAllWindows()
