###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: args.py
# Project: Security System
# Description:
#   implement command line options for configuring security camera and recordings
# Last Modified: 7.18.2016
###############################################################################
import argparse

# Initialize argument parser
parser = argparse.ArgumentParser()

# command line options
parser.add_argument("-l", "--length", help="number of frames to record upon person detection", type=int, default=1000)
parser.add_argument("-f", "--fps", help="framerate of video recording", default=20, type=int)
parser.add_argument("-u", "--url", help="IP camera location url", type=str)
parser.add_argument("-c", "--camera", help="location of USB camera", default=0, type=int)
parser.add_argument("-ht", "--height", help="video recording height", default=480, type=int)
parser.add_argument("-w", "--width", help="video recording width", default=640, type=int)
parser.add_argument("-k", "--cascade", help="HOG cascade classifier filename", type=str, default="hog.xml")
parser.add_argument("-s", "--scale", help="adjust the scale factor", default=1.05, type=float)
parser.add_argument("-d", "--debug", help="turn on debug mode", action="store_true")
parser.add_argument("-v", "--visual", help="turn on visual mode", action="store_true")
parser.add_argument("-r", "--record", help="enable recording", action="store_true")
parser.add_argument("-m", "--message", help="enable MQTT transmission", action="store_true")



args = parser.parse_args()

message = args.message
scale = args.scale
# set variable values from options
recordLength = args.length
display = args.visual
# check if given URL or USB camera
if args.url:
    dest = args.url
else:
    dest = args.camera

# cascade path
cascPath = args.cascade
# scaling factor used in cascade parameters
scaleFactor = args.scale

# frame dimensions
frameHeight = args.height
frameWidth = args.width

# recording frame rate
frameRate = args.fps
debug = args.debug
visual = args.visual
record = args.record
