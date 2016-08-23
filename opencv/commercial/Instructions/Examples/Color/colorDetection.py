"""
Display three views:
    original frame
    mask
    resultant frame
whenever user clicks in original frame, color is specified
this color becomes the new mask color
The system then creates a contour around the largest object of that color on the screen, and a crosshair follows after that object
"""

import cv2
import numpy as np

begin = False


def drawXHair( img, x, y ):
    "draws crosshair at specified point"
    color = ( 0, 0, 255 )
    radius = 20
    thickn = 2
    cv2.circle( img, ( int( x ), int( y ) ), 20, color, thickn )
    cv2.line( img, ( x-radius, y ), ( x+radius, y ), color, thickn )
    cv2.line( img, ( x, y-radius ), ( x, y+radius ), color, thickn )

# Callbacks

def colorSelect( event, x, y, flags, param ):
    "click to select color"
    global color, begin
    if event == cv2.EVENT_LBUTTONUP:
        if not begin:
            begin = True
        color_bgr = frame[y, x, :]
        color = cv2.cvtColor(  np.uint8(  [[color_bgr]]  ), cv2.COLOR_BGR2HSV  )

def doNothing( x ):
    "does nothing"
    pass


cv2.namedWindow( 'Track Color Object' )
cv2.setMouseCallback( 'Track Color Object', colorSelect )

cv2.createTrackbar( 'dH', 'Track Color Object', 10, 50, doNothing )
cv2.createTrackbar( 'dS', 'Track Color Object', 10, 50, doNothing )
cv2.createTrackbar( 'dV', 'Track Color Object', 10, 50, doNothing )
# begin the video capture
cap = cv2.VideoCapture( 0 )
while( 1 ):
    dh = cv2.getTrackbarPos( 'dH', 'Track Color Object' )
    ds = cv2.getTrackbarPos( 'dS', 'Track Color Object' )
    dv = cv2.getTrackbarPos( 'dV', 'Track Color Object' )

    # create the color range array from these values
    cRanArr = np.array( [dh, ds, dv] )
    # take each frame
    _, frame = cap.read(  )
    if begin:
        # convert BGR to HSV
        hsv = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV )

        # define range of  color in HSV
        lower_color = color - cRanArr
        upper_color = color + cRanArr

        # threshold the HSV image to only get colors wi specified range
        mask = cv2.inRange( hsv, lower_color, upper_color )

        # Morphological Noise Removal
        kernel = np.ones( ( 20,20 ), np.uint8 )
        # mask = cv2.dilate( mask, kernel, iterations=1 )
        mask = cv2.morphologyEx( mask, cv2.MORPH_CLOSE, kernel )
        disk = cv2.getStructuringElement(  cv2.MORPH_ELLIPSE, (  35,35  )  )
        mask = cv2.filter2D(  mask, -1, disk )

        # cv2.imshow( 'mask',mask )

        # find contours from the mask
        im, contours, hierarchy = cv2.findContours( mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

        # if contours are available, draw a crosshair on the centroid of the largest contour
        if len( contours )>0:
            # detect the largest contour
            area = 0

            for i in contours:
                # find the largest area contour
                cnt_ar = cv2.contourArea( i )
                if cv2.contourArea( i )>area:
                    largest_contour = i
                    area = cnt_ar
            # find moment of contour
            M = cv2.moments( largest_contour )
                # find contour centroid
            cx = int( M['m10']/( M['m00'] ) )
            cy = int( M['m01']/( M['m00'] ) )
            # cv2.drawContours( frame, largest_contour, -1, ( 255, 255, 0 ) )
            drawXHair( frame, cx, cy )

    cv2.imshow( 'Track Color Object', frame )


    # if user presses escape key, exit
    if cv2.waitKey( 1 ) == 27:
        break
cap.release(  )
cv2.destroyAllWindows(  )
