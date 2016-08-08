###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: motion_detection_stat.py
# Project: Security System
# Description:
#   detect motion in a static room using standard deviations
# Last Modified: 7.25.2016
###############################################################################
import numpy as np
import cv2
import utils


if utils.visual:
    cv2.namedWindow('frame')
    cv2.namedWindow('dist')


cap = cv2.VideoCapture(0)

DISP_STDEV = True
DEBUG = utils.debug # enters noise mode

calcSDAvg = False

sdList = np.array([])
triggered = False


def stAvgSelect(event, x, y, flags, param):
    global calcSDAvg, sdList, sdAvg
    if event == cv2.EVENT_LBUTTONDOWN:
        if not calcSDAvg:
            sdList = np.array([])
            calcSDAvg = True
            print "Click again to set average standard deviation"
        else:
            calcSDAvg = False
            sdAvg = np.mean(sdList)
            print "The mean standard deviation is {}".format(sdAvg)



if utils.sdAvg:
    sdAvg = utils.sdAvg
else:
    sdAvg = 2.5
    cv2.setMouseCallback('frame', stAvgSelect)
    print "Click to begin capturing average standard deviation"

if utils.record:
    # create the VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG') # MJPG is encoding supported by Windows
    # create output video file name
    fname = utils.currDate() + "_" + utils.currTime() + ".avi"
    # configure output video settings
    out = cv2.VideoWriter(fname, fourcc, utils.frameRate, (utils.frameWidth, utils.frameHeight))
else:
    fname = ''


_, frame1 = cap.read()
_, frame2 = cap.read()

frameCount = 1
lastStart = -1
while(True):
    _, frame3 = cap.read()
    rows, cols, _ = np.shape(frame3)
    if DEBUG:
        frame3 = utils.applyNoise(frame3, utils.noise)
    dist = utils.distMap(frame1, frame3)

    frame1 = frame2
    frame2 = frame3

    # apply Gaussian smoothing
    mod = cv2.GaussianBlur(dist, (9,9), 0)

    # apply thresholding
    _, thresh = cv2.threshold(mod, 100, 255, 0)
    edge = cv2.Canny(mod, 100, 255)

    # edge = cv2.Canny(dist, 100, 255)


    # mean and st dev test
    mean, stDev = cv2.meanStdDev(mod)
    # print stDev

    if calcSDAvg:
        sdList = np.append(sdList, stDev)
    else:
        if stDev > sdAvg + utils.sdThresh:
            if not triggered:

                lastStart = frameCount

                triggerInfo = {
                    "event": "MotionDetect",
                    "uri": "http://gateway" + "/" + fname,
                    "timestamp": utils.currDate() + "--" + utils.currTime(),
                    "offsetframe": lastStart
                    }

                utils.trigger(triggerInfo)
                triggered = True
        else:
            triggered = False
    if utils.record and (frameCount - lastStart) < utils.recordLength:
        out.write(frame2)
        frameCount += 1
    if utils.visual:
        cv2.imshow('dist', mod)
        cv2.imshow('edge', edge)
        cv2.imshow('frame', frame2)

    # easier to see for DEBUG
    blank = np.ones(np.shape(frame3))
    if utils.visual:
        if DISP_STDEV:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(blank, "{}".format(stDev[0][0]), (cols/8, rows/2), font, 5, (0, 0, 255), 3, cv2.LINE_AA)
            cv2.imshow("stDev", blank)


    if cv2.waitKey(1) & 0xFF == 27:
        break

if utils.record:
    out.release()
cap.release()
cv2.destroyAllWindows()
