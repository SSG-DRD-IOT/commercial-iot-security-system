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
# while cap.isOpened == False:
#     print ' '
# print 'cap.isOpened is ', cap.isOpened
_, frame = cap.read()
# print 'ret is ', ret
# while ret == False:
#     print ''
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
    cv2.imshow('blob', blobby)
    # buffer
    pastBuff = currBuff
    currBuff = ( (currBuff << 1) | (np.any(blobby)) ) & buffMask

    fra, contours, hierarchy = cv2.findContours(blobby, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # print np.shape(blobby)
    area = 0
    largest_contour = -1
    for i in xrange(len(contours)):
        if cv2.contourArea(contours[i])>area:
            largest_contour = i
    #
    # cv2.drawContours(blobby, contours, 0, 150,  3)
    frameMod = np.copy(frame)
    cv2.drawContours(frameMod, contours, largest_contour, [0, 0, 255],  3)
    # if largest_contour > -1:
    #     rect = cv2.minAreaRect(contours[0])
    #     box = cv2.boxPoints(rect)
    #     box = np.int0(box)
    #     cv2.drawContours(frameMod, [box], 0, (0, 0, 255), 2)
    #
    # cv2.drawContours(blobby, contours, -1, 150,  3)
    # minArea = 0
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # if len(contours) > 1:
        # print cv2.contourArea(contours[largest_contour])
        # if cv2.contourArea(contours[largest_contour]) > minArea:
            # cv2.drawContours(frameMod, contours, 0, [150, 0, 0],  3)
            # cv2.putText(frameMod, 'CONTOUR_DET', (10,500), font, 4, (0, 0, 255), 5, cv2.LINE_AA)
    # cv2.drawContours(blobby, contours, -1, 150,  3)
    # cv2.drawContours(blobby, contours, i, 150,  3)

    if currBuff == buffMask:
        cv2.imshow('frame', frameMod)
        # cv2.imshow('blobby', blobby)
        # cv2.imshow('frame', blobby)
    else:
        cv2.imshow('frame', frame)
    # cv2.imshow('blob', blobby)
    cv2.imshow('fra', fra)
    # print np.any(blobby)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
