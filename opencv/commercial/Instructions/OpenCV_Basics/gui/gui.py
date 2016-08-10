import cv2
import numpy as np

def drawCircle( event, x, y, flags, param ):
    global tempCircle, circlesList
    circ = {
        "coord": (x, y),
        "radius": param
    }
    if event == cv2.EVENT_LBUTTONUP:
        circlesList.append(circ)
        print circlesList
    elif event == cv2.EVENT_MOUSEMOVE:
        tempCircle = circ

def setRadius(radius):
    cv2.setMouseCallback( "New Window", drawCircle, radius)

tempCircle = False
circlesList = []
radius = 5

cv2.namedWindow( "New Window" )
cv2.setMouseCallback( "New Window", drawCircle, radius)
cv2.createTrackbar('Radius', 'New Window', 0, 255, setRadius)

while(True):
    img = np.zeros( (480, 640, 3), np.uint8 )
    # cv2.getTrackbarPos('Radius', 'New Window')
    if tempCircle:
        cv2.circle( img, tempCircle["coord"], tempCircle["radius"], (0, 255, 0), 5 )
    for circle in circlesList:
        cv2.circle( img, circle["coord"], circle["radius"], (0, 255, 0), -1 )
    cv2.imshow( "New Window", img )

    k = cv2.waitKey(1)
    if k == 27: # ESC
        break
    elif k == ord('s'):
        cv2.imwrite("new_drawing.jpg", img)

cv2.destroyAllWindows()
