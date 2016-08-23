import numpy as np
import cv2

xi, yi, xf, yf = 0, 0, 0, 0
selecting = False
newHist = False
begin = False
def regionSelect( event, x, y, flags, param ):
    global xi, yi, xf, yf, selecting, newHist, begin
    if event == cv2.EVENT_LBUTTONDOWN:
        selecting = True
        xi, yi = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        xf, yf = x, y
        selecting = False
        newHist = True
        begin = True

cap = cv2.VideoCapture( 0 )

cv2.namedWindow( 'frame' )
cv2.setMouseCallback( 'frame', regionSelect )

while( True ):
    if not selecting:
        _, frame = cap.read()
        if begin:
            hsv = cv2.cvtColor(  frame, cv2.COLOR_BGR2HSV )
            mask = np.zeros( frame.shape[:2], np.uint8 )
            mask[min( yi, yf ) : max( yi, yf ), min( xi, xf ):max( xi, xf )] = 255
            if newHist:
                roiHist = cv2.calcHist( [hsv], [0, 1], mask, [180, 256], [0, 180, 0, 256] )
                roiHist = cv2.normalize( roiHist, roiHist, 0, 255, cv2.NORM_MINMAX )
                newHist = False

            targetHist = cv2.calcHist( [hsv], [0, 1], None, [180, 256], [0, 180, 0, 256] )

            dst = cv2.calcBackProject( [hsv], [0, 1], roiHist, [0, 180, 0, 256], 1 )

            disk = cv2.getStructuringElement( cv2.MORPH_ELLIPSE, ( 15,15 ) )
            dst = cv2.filter2D( dst, -1, disk )
            prox = np.copy( dst )

            # # threshold and binary AND
            _, thresh = cv2.threshold( dst, 250, 255, 0 )

            kernel = cv2.getStructuringElement( cv2.MORPH_ELLIPSE, ( 5,5 ) )

            thresh = cv2.erode( thresh, kernel, iterations = 3 )
            thresh = cv2.dilate( thresh, kernel, iterations= 3 )

            masked_dots = cv2.bitwise_and( prox, prox, mask = thresh )

            # prox = cv2.applyColorMap( prox, cv2.COLORMAP_JET )
            masked_dots = cv2.applyColorMap( masked_dots, cv2.COLORMAP_JET )

            cv2.imshow( 'distance', masked_dots )

    cv2.imshow( 'frame', frame )
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
