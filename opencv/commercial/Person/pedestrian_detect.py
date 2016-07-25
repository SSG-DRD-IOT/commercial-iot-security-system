###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: pedestrian_detect.py
# Project: Security System
# Description:
#   detects pedestrians on a street using HOG cascade
#   uses hog.xml for cascade
# Last Modified: 7.18.2016
###############################################################################
"""Usage:\tpython pedestrian_detect.py [-u pedestrians.mp4] [options]"""
import numpy as np
import cv2
import utils

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def drawDetected(frame, rects):
    for x, y, w, h in rects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

print utils.dest, type(utils.dest)
cap = cv2.VideoCapture(utils.dest)
# TODO: differentiate between camera and online input
    # also find difference between reading from video and IP Camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH,utils.frameHeight)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,utils.frameWidth)

if utils.record:
    # create the VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG') # MJPG is encoding supported by Windows
    # create output video file name
    fname = utils.currDate() + "_" + utils.currTime() + ".avi"
    # configure output video settings
    out = cv2.VideoWriter(fname, fourcc, utils.frameRate, (utils.frameWidth, utils.frameHeight))

personCount = 0
frameCount = 0
lastStart = -1
if utils.debug:
    print "debug mode turned on\n"
if utils.visual:
    print "visual mode turned on\n"

while(cap.isOpened()):
    _, frame = cap.read()
    found, w = hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05, hitThreshold = .71)
    found_filtered = []
    for ri, r in enumerate(found):
        for qi, q in enumerate(found):
            if ri != qi and inside(r, q):
                break
        else:
            found_filtered.append(r)

    if len(found_filtered) != personCount:
        personCount = len(found_filtered)
        print "number of people changed"
        triggerInfo = {
            "event": "PersonDetect",
            "facenum": len(found_filtered),
            "timestamp": utils.currDate() + "--" + utils.currTime()
        }
        if utils.record:
            triggerInfo['uri'] = "http://gateway" + "/" + fname
            triggerInfo['offsetframe'] = frameCount
        # activate a trigger, which transmits via MQTT
        utils.trigger(triggerInfo)
        lastStart = frameCount

    if utils.visual:
        drawDetected(frame, found_filtered)
        cv2.imshow('video', frame)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            cap.release()
            cv2.destroyAllWindows()
            break
    if utils.record and (frameCount - lastStart) < utils.recordLength:
        out.write(frame)
        frameCount += 1
    if utils.debug:
        print('%d (%d) found' % (len(found_filtered), len(found)))
if utils.record:
    out.release()
