
import numpy as np
import cv2

def setEmpty(event, x, y, flags, param):
    global emptyFrame, emptyFrame32
    if event == cv2.EVENT_LBUTTONDOWN:
        emptyFrame = frame
        print('single')
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        emptyFrame = np.zeros(np.shape(frame), np.uint8)
        print('double')
    emptyFrame32 = np.float32(emptyFrame)

cap = cv2.VideoCapture(0)
_, frame = cap.read()
emptyFrame = np.zeros(np.shape(frame), np.uint8)
emptyFrame32 = np.float32(emptyFrame)

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', setEmpty)

while(True):
    _, frame = cap.read()
    frame32 = np.float32(frame)
    # diff = frame - emptyFrame
    diff32 = np.absolute(frame32 - emptyFrame32)
    # print(np.max(diff32))
    # print(diff32)
    # print(np.max(diff32))
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    # # for i in xrange(3):
    #     # print i,':'
    #     # print np.shape(diff32[:,:,i])
    diff = np.uint8(norm32*255)
    _, thresh = cv2.threshold(diff, 100, 255, 0)
    kernel = np.ones((20,20), np.uint8)
    blobby = cv2.dilate(thresh, kernel, iterations= 4)
    # diff = np.uint8(np.round(diff32))
    # diff = np.uint8(diff32)
    # print(np.max(diff))
    # cv2.imshow('frame', frame)
    # cv2.imshow('diff', diff)
    # print(diff)
    # print(np.max(diff))
    cv2.imshow('frame', blobby)
    # cv2.imshow('orig', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
