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
        # numBytes = 163840
        # numBytes = 63840
        numBytes = 13840
        self.bytes += self.stream.read(numBytes)
        # print self.bytes
        a = self.bytes.find('\xff\xd8')
        # print a
        b = self.bytes.find('\xff\xd9')
        # print b
        if a != -1 and b != -1:
            jpg = self.bytes[a:b+2]
            self.bytes = self.bytes[b+2:]
            self.frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            # print self.frame
            # return self.frame
        return self.frame

def findHSV(bgr):
    "convert BGR array to HSV"
    bgr = np.uint8([[bgr]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    return hsv

def drawXHair(img, y, x):
    # 20 pt radius
    color = (0 ,0, 255)
    # color = tuple(col[0][0])
    # print type(col)
    # print(col)
    radius = 20
    thickn = 2
    cv2.circle(img, (int(x), int(y)), 20, color, thickn)
    cv2.line(img, (x - radius, y), (x + radius, y), color, thickn)
    cv2.line(img, (x, y - radius), (x, y + radius), color, thickn)


def colorSelect(event, x, y, flags, param):
    global color
    if event == cv2.EVENT_LBUTTONUP:
        color_rgb = frame[y, x, 0:3]
        color = findHSV(color_rgb)
        print(color)
