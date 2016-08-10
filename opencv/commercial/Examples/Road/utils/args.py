###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: args.py
# Project: Car Speed Detection
# Description:
#   implement command line options for configuring traffic camera and recordings
# Last Modified: 8.3.2016
###############################################################################
import argparse

# Initialize argument parser
parser = argparse.ArgumentParser()

# command line options
parser.add_argument("-i", "--input", help="pickle file containing ROI and dash parameters", type=str, default='points.pickle')
parser.add_argument("-l", "--length", help="number of frames to record upon speeding detect", type=int, default=30)
parser.add_argument("-f", "--fps", help="framerate of video recording", default=20, type=int)
parser.add_argument("-b", "--buffer", help="calibrate buffer length", default=30, type=int)
parser.add_argument("-u", "--url", help="IP camera location url", type=str, default="carsCrop.avi")
parser.add_argument("-c", "--camera", help="location of USB camera", type=int)
parser.add_argument("-d", "--debug", help="turn on debug mode", action="store_true")
parser.add_argument("-v", "--visual", help="turn on visual mode", action="store_true")
parser.add_argument("-r", "--record", help="enable recording", action="store_true")
parser.add_argument("-t", "--triggers", help="toggle MQTT triggers", action="store_true")
parser.add_argument("-x", "--displacement", help="set minimum displacement", type=int, default=2)
parser.add_argument("--inf", help="Loop video infinitely", action="store_true")


args = parser.parse_args()

# Minimum displacement threshold
x_thresh = args.displacement

# loop over video infinitely
inf = args.inf

# ROI and dash input parameters
inputParams = args.input

# set variable values from options
BUFF_LEN = args.buffer
recordLength = args.length
display = args.visual
# check if given URL or USB camera
if args.camera == None:
    dest = args.url
else:
    dest = args.camera

# recording frame rate
frameRate = args.fps
debug = args.debug
visual = args.visual
record = args.record
triggers = args.triggers
