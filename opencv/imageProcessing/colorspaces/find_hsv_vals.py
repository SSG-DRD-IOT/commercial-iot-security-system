"""
find HSV values to track
use cv2.cvtColor()
instead of passing image, pass the BGR vals you want
"""

# ex. to find the HSV value of Green, try:
green = np.uint8([[[0,255,0]]])
hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
print hsv_green # [[[ 60 255 255 ]]]
# now take [H-10, 100, 100] and [H+10, 255, 255] as lower and upper bound respectively
