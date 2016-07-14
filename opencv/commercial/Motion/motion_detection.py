import numpy as np
import cv2
import utils

def setEmpty(event, x, y, flags, param):
    global emptyFrame, emptyFrame32
    if event == cv2.EVENT_LBUTTONDOWN:
        emptyFrame = frame
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        emptyFrame = np.zeros(np.shape(frame), np.uint8)
    emptyFrame32 = np.float32(emptyFrame)


BUFF_LEN = 5
buffMask = utils.genBuffMask(BUFF_LEN)
currBuff = 0

if len(utils.argv) > 1:
    dest = utils.argv[1]
else:
    dest = '0'

if len(dest) > 4:
    cap = utils.OnlineVideo(dest)
else:
    cap = cv2.VideoCapture(int(dest))


_, frame = cap.read()

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

    fra, contours, hierarchy = cv2.findContours(blobby, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    area = 0
    largest_contour = -1
    for i in xrange(len(contours)):
        if cv2.contourArea(contours[i])>area:
            largest_contour = i

    frameMod = np.copy(frame)
    cv2.drawContours(frameMod, contours, largest_contour, [0, 0, 255],  3)

    # buffer
    pastBuff = currBuff
    currBuff = ( (currBuff << 1) | (np.any(blobby)) ) & buffMask
    if currBuff == buffMask:
        cv2.imshow('frame', frameMod)
    else:
        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
    # elif cv2.waitKey(1) & 0xFF == ord('r'):
    #     cap.release()
    #     cap = OnlineVideo(url)
    #     print('retarting')
cap.release()
cv2.destroyAllWindows()
