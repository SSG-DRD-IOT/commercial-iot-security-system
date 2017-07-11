import cv2
import sys

# Create a Haar-like feature cascade classifier object
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Set the camera to the first camera detected by the NUC
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # begin face cascade
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.25,
        minNeighbors=5,
        minSize=(30, 30),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # If the user presses the 'q' key then quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

# When everything is done, release the capture
cv2.destroyAllWindows()
