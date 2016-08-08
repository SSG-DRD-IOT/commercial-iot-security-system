import cv2
import numpy as np

cap = cv2.VideoCapture( 0 )
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
fps = 24
width, height = ( 640, 480 )
out = cv2.VideoWriter( 'output.avi', fourcc, fps, ( width, height ) )
while( True ):
	ret, frame = cap.read()
	out.write( frame )
	cv2.imshow( "Video", frame )
	k = cv2.waitKey(1)
	if k == ord( 'q' ):
		break

cap.release()
out.release()
