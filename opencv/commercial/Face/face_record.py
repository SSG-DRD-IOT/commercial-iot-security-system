import cv2
import utils

buffMask = utils.genBuffMask(utils.BUFF_LEN)

faceCascade = cv2.CascadeClassifier(utils.cascPath)


cap = cv2.VideoCapture(utils.dest)

# create the VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG') # MJPG is encoding supported by Windows

fname = utils.currDate() + "_" + utils.currTime() + ".avi"
out = cv2.VideoWriter(fname, fourcc, utils.frameRate, (utils.frameWidth, utils.frameHeight))

currBuff = 0

# the number of the frame in the video
frameCount = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # the cascade works in grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # begin face cascade
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.25,
        minNeighbors=5,
        minSize=(30, 30)
    )


    # updates current buffer
    pastBuff = currBuff
    currBuff = ( (currBuff << 1) | (len(faces)>0) ) & buffMask

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)

    if(currBuff == 1):
        triggerInfo = {
            "event": "FaceDetect",
            "uri": "http://gateway" + "/" + fname,
            "facenum": len(faces),
            "timestamp": utils.currDate() + "--" + utils.currTime(),
            "offsetframe": frameCount
        }
        utils.trigger(triggerInfo)
        lastStart = frameCount

    if( (currBuff > 0) ):
        if (frameCount - lastStart) < utils.recordLength:
            out.write(frame)
        frameCount += 1


    # Display the resulting frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
out.release()
cap.release()
cv2.destroyAllWindows()
