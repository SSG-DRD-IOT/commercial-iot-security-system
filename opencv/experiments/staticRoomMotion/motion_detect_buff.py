import numpy as np
import cv2
from sys import argv
import urllib

def setEmpty(event, x, y, flags, param):
    global emptyFrame, emptyFrame32
    if event == cv2.EVENT_LBUTTONDOWN:
        emptyFrame = frame
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        emptyFrame = np.zeros(np.shape(frame), np.uint8)
    emptyFrame32 = np.float32(emptyFrame)

def genBuffMask(bufferFrames):
    'create bitwise mask for buffer length'
    buffMask = 1
    for i in range(0, BUFF_LEN-1):
        buffMask = (buffMask)<<1 | buffMask
    return buffMask
BUFF_LEN = 10
buffMask = genBuffMask(BUFF_LEN)
currBuff = 0

# if len(argv) > 1:
#     videoLocation = argv[1]
#     print argv[1]
# else:
#     videoLocation = 0
videoLocation = 0


cap = cv2.VideoCapture(videoLocation)
while cap.isOpened == False:
    print ' '
print 'cap.isOpened is ', cap.isOpened
ret, frame = cap.read()
print 'ret is ', ret
while ret == False:
    print ''
# print np.shape(frame)
blankFrame = np.zeros(np.shape(frame), np.uint8)
emptyFrame = blankFrame
emptyFrame32 = np.float32(blankFrame)

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', setEmpty)

while(True):
    _, frame = cap.read()
    frame32 = np.float32(frame)

    diff32 = np.absolute(frame32 - emptyFrame32)

    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)

    diff = np.uint8(norm32*255)
    _, thresh = cv2.threshold(diff, 100, 255, 0)
    kernel = np.ones((20,20), np.uint8)
    blobby = cv2.dilate(thresh, kernel, iterations= 4)

    # buffer
    pastBuff = currBuff
    currBuff = ( (currBuff << 1) | (np.any(blobby)) ) & buffMask
    if currBuff == buffMask:
        cv2.imshow('frame', blobby)
    else:
        cv2.imshow('frame', blankFrame)
    # print np.any(blobby)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
