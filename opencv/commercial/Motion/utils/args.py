###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: args.py
# Project: Security System
# Description:
#   implement command line options for configuring security camera and recordings
# Last Modified: 7.25.2016
###############################################################################
import argparse

# Initialize argument parser
parser = argparse.ArgumentParser()

# command line options
parser.add_argument("-l", "--length", help="number of frames to record upon detection", type=int, default=1000)
parser.add_argument("-f", "--fps", help="framerate of video recording", default=20, type=int)
parser.add_argument("-b", "--buffer", help="calibrate buffer length", default=30, type=int)
parser.add_argument("-u", "--url", help="IP camera location url", type=str)
parser.add_argument("-c", "--camera", help="location of USB camera", default=0, type=int)
parser.add_argument("-ht", "--height", help="video recording height", default=480, type=int)
parser.add_argument("-w", "--width", help="video recording width", default=640, type=int)
parser.add_argument("-t", "--threshold", help="set threshold value", default=2.0, type=float)
parser.add_argument("-v", "--visual", help="turn on visual mode", action="count")
parser.add_argument("-n", "--noise", help="set noise multiplier", default=.005, type=float)
parser.add_argument("-d", "--debug", help="turn on debug mode", action="count")
parser.add_argument("-s", "--stdev", help="set average st dev", default=0, type=float)
parser.add_argument("-r", "--record", help="enable recording", action="count")

args = parser.parse_args()

visual = args.visual
record = args.record

sdAvg = args.stdev
sdThresh = args.threshold
noise = args.noise # scaling of noise; 0-1
debug = args.debug
# set variable values from options
BUFF_LEN = args.buffer
recordLength = args.length

# check if given URL or USB camera
if args.url:
    dest = args.url
else:
    dest = args.camera


# frame dimensions
frameHeight = args.height
frameWidth = args.width
# recording frame rate
frameRate = args.fps
