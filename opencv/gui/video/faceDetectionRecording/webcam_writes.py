import cv2
import sys

print sys.argv, len(sys.argv)
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
if len(sys.argv)==3:
    if sys.argv[2] == 0:
        camera = 0
    elif sys.argv[2] == 1:
        camera = 1
    else:
        camera = 0
else:
    camera = 0
cap = cv2.VideoCapture(0)
# create the VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# triggers if a face is seen
seesFace = False

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.25,
        #scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # checks whether there is a face in the frame
    sawFace = seesFace
    seesFace = len(faces)>0

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
    if(seesFace):
        # print "seen"
        out.write(frame)
    elif(~seesFace & sawFace):
        # print "nope"
        break
    # Display the resulting frame
    cv2.imshow('Video', frame)
    # cv2.imshow('Video', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
out.release()
cap.release()
cv2.destroyAllWindows()
