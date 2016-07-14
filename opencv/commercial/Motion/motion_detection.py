###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: motion_detection.py
# Project: Security System
# Description:
#   detect motion in a static room
# Last Modified: 7.14.2016
###############################################################################
import numpy as np
import cv2
import utils

def setEmpty(event, x, y, flags, param):
    global emptyFrame, emptyFrame32
    if event == cv2.EVENT_LBUTTONDOWN:
        emptyFrame = frame
    emptyFrame32 = np.float32(emptyFrame)

buffMask = utils.genBuffMask(utils.BUFF_LEN)

currBuff = 0

if type(utils.dest) is str:
    cap = utils.OnlineVideo(utils.dest)
else:
    cap = cv2.VideoCapture(utils.dest)


_, frame = cap.read()

emptyFrame = np.zeros(np.shape(frame), np.uint8)
emptyFrame32 = np.float32(emptyFrame)

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', setEmpty)

while(True):
    _, frame = cap.read()
    frame32 = np.float32(frame)

    diff32 = frame32 - emptyFrame32

    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)

    diff = np.uint8(norm32*255)
    _, thresh = cv2.threshold(diff, 100, 255, 0)
    kernel = np.ones((20,20), np.uint8)
    blobby = cv2.dilate(thresh, kernel, iterations= 4)

    fra, contours, hierarchy = cv2.findContours(blobby, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    area = 0
    for i in xrange(len(contours)):
        if cv2.contourArea(contours[i])>area:
            largest_contour = i

    frameMod = np.copy(frame)
    cv2.drawContours(frameMod, contours, largest_contour, [0, 0, 255],  3)

    # buffer
    currBuff = ( (currBuff << 1) | (np.any(blobby)) ) & buffMask
    if currBuff == 1:
        # temp ###
        fname = "file.avi"
        # / ######
        # dictionary stores data to be transmitted
        triggerInfo = {
            "event": "MotionDetect",
            "uri": "http://gateway" + "/" + fname,
            "timestamp": utils.currDate() + "--" + utils.currTime()
            # "offsetframe": frameCount
        }
        # activate a trigger, which transmits via MQTT
        utils.trigger(triggerInfo)
    if currBuff == buffMask:
        cv2.imshow('frame', frameMod)
    else:
        cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
