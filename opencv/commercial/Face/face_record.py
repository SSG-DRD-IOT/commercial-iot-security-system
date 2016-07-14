import cv2
import utils

BUFF_LEN = 30 # 30 seems to be optimal number of frames for buffer

buffMask = utils.genBuffMask(BUFF_LEN)

if len(utils.argv) > 1:
    cascPath = utils.argv[1]
else:
    cascPath = 'haar_face.xml'

faceCascade = cv2.CascadeClassifier(cascPath)

# input which camera to use
if len(utils.argv)==3:
    if utils.argv[2] == 0:
        camera = 0
    elif utils.argv[2] == 1:
        camera = 1
    else:
        camera = 0
else:
    camera = 0

cap = cv2.VideoCapture(0)

# create the VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG') # MJPG is encoding supported by Windows

i = 0
out = cv2.VideoWriter('output'+str(i)+'.avi', fourcc, 20.0, (640, 480))

currBuff = 0;

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()

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
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if(currBuff > 0):
        out.write(frame)
    if(currBuff == 1):
        utils.trigger(len(faces))
    elif((pastBuff>0) & (currBuff == 0)): # after face detected, of face disappears for BUFF_LEN frames, stop recording
        out.release()
        i = i + 1
        out = cv2.VideoWriter('output'+str(i)+'.avi', fourcc, 20.0, (640, 480))

    # Display the resulting frame
    cv2.imshow('Video', frame)
    # cv2.imshow('Video', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
out.release()
cap.release()
cv2.destroyAllWindows()
