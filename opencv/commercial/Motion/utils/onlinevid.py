###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: onlinevid.py
# Project: Security System
# Description:
#   class for online video streaming
#   OpenCV's built-in VideoCapture breaks when given URL
#   this class opens a stream and parses out every frame of the video
# Last Modified: 7.14.2016
###############################################################################
import numpy as np
import cv2
import urllib

class OnlineVideo(object):
    """
    USAGE:
    cap = OnlineVideo(url)
        ex. OnlineVideo('http://IP_ADDRESS:PORT/video.mjpg')
    frame = cap.read()

    see: http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera
    """

    # open the url
    def __init__(self, url):
        self.stream = urllib.urlopen(url)
        self.bytes = ''
        self.frame = np.zeros((480, 640, 3), np.uint8)
        print "url opened at: ", url
    # read data frame-by-frame
    def read(self):
        # read data by chunks
        numBytes = 13840
        self.bytes += self.stream.read(numBytes)
        # parse achunk
        a = self.bytes.find('\xff\xd8')
        b = self.bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = self.bytes[a:b+2]
            self.bytes = self.bytes[b+2:]
            self.frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        # return frame availability and frame
        return bool(self.frame), self.frame
    # stop online stream
    def release(self):
        self.stream.close()
