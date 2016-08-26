###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: face_record.py
# Project: Security System
# Description:
#   face recording component
#       use a Haar cascade to identify faces
#       once face is detected, record for a certain number of frames
# Last Modified: 7.14.2016
###############################################################################
import cv2
import utils

# a buffer smoothes out flickering in the facial recognition
# genBuffMask generates a sequence of continuous binary 1's
buffMask = utils.genBuffMask(utils.BUFF_LEN)

# the classifier that will be used in the cascade
faceCascade = cv2.CascadeClassifier(utils.cascPath)

# use to select video source
cap = cv2.VideoCapture(utils.dest)


if utils.record:
    # create the VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG') # MJPG is encoding supported by Windows
    # create output video file name
    fname = utils.currDate() + "_" + utils.currTime() + ".avi"
    # configure output video settings
    out = cv2.VideoWriter(fname, fourcc, utils.frameRate, (utils.frameWidth, utils.frameHeight))

# create a fresh buffer
currBuff = 0

# the number of the frame in the video
frameCount = 0
lastStart = -1
while True:
    # Capture frame-by-frame
    _, frame = cap.read()

    # the cascade is implemented in grayscale mode
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # begin face cascade
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=utils.scaleFactor,
        minSize=(20, 20)
    )
    # draw a rectangle over detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)

    # updates current buffer
    currBuff = ( (currBuff << 1) | (len(faces)>0) ) & buffMask


    # if a face was detected after extemded period of time, transmit information
    if(currBuff == 1):
        # dictionary contains data to be transmitted
        triggerInfo = {
            "event": "FaceDetect",
            "facenum": len(faces),
            "timestamp": utils.currDate() + "--" + utils.currTime()
        }
        if utils.record:
            triggerInfo['offsetframe'] = frameCount
            triggerInfo['uri'] = "http://gateway" + "/" + fname
            # start counting frames since seeing face
            lastStart = frameCount
        # activate a trigger, which transmits via MQTT
        utils.trigger(triggerInfo)

    # write to video file if buffer active
    if(currBuff > 0):
        # only writes if amount of time since face detection less than set recorging length
        if ( (frameCount - lastStart) < utils.recordLength ) and utils.record:
            out.write(frame)
        frameCount += 1


    # Display the resulting frame
    if utils.visual:
        cv2.imshow('Video', frame)
    # press q to quit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# When everything is done, release the capture
if utils.record:
    out.release()
cap.release()
cv2.destroyAllWindows()
