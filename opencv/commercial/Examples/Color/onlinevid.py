import numpy as np
import cv2
import urllib

class OnlineVideo(object):
    """
    USAGE:
    cap = OnlineVideo(url)
        ex. OnlineVideo('http://IP_ADDRESS:PORT/video.mjpg')
    frame = cap.getFrame()

    see: http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera
    """
    def __init__(self, url):
        self.stream = urllib.urlopen(url)
        self.bytes = ''
        self.frame = np.zeros((480, 640, 3), np.uint8)
        print "url opened at: ", url
    def getFrame(self):
        numBytes = 13840
        self.bytes += self.stream.read(numBytes)
        a = self.bytes.find('\xff\xd8')
        b = self.bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = self.bytes[a:b+2]
            self.bytes = self.bytes[b+2:]
            self.frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        return self.frame
    def killStream(self):
        self.stream.close()
