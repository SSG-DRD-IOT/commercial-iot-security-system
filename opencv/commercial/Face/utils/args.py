import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-l", "--length", help="number of frames to record upon face detect", type=int, default=1000)
parser.add_argument("-f", "--fps", help="framerate of video recording", default=20, type=int)
parser.add_argument("-b", "--buffer", help="calibrate face detection buffer length", default=30, type=int)
parser.add_argument("-u", "--url", help="IP camera location url", type=str)
parser.add_argument("-c", "--camera", help="location of USB camera", default=0, type=int)
parser.add_argument("-ht", "--height", help="video recording height", default=480, type=int)
parser.add_argument("-w", "--width", help="video recording width", default=640, type=int)
parser.add_argument("-k", "--cascade", help="Haar cascade classifier filename", type=str, default="haar_face.xml")

args = parser.parse_args()

BUFF_LEN = args.buffer
recordLength = args.length

if args.url:
    dest = args.url
else:
    dest = args.camera

cascPath = args.cascade

frameHeight = args.height
frameWidth = args.width
frameRate = args.fps
################################################################################
# For Testing
################################################################################
# print "buffer length:\t", BUFF_LEN, type(BUFF_LEN)
# print "recording length:\t", recordLength, type(recordLength)
# print "dest\t:", dest, type(dest)
# print "frame height:\t", frameHeight, type(frameHeight)
# print "frame width:\t", frameWidth, type(frameWidth)
# print "frame rate:\t", frameRate, type(frameRate)
