import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while(True):
_, frame = cap.read()
    mask = np.zeros(img.shape[:2], np.uint8)
    # display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# when everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
