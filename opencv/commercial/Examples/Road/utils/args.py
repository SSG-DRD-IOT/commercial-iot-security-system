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
import os.path as path
import platform
# Initialize argument parser
parser = argparse.ArgumentParser()

# command line options
parser.add_argument("-i", "--input", help="pickle file containing ROI and dash parameters", type=str, default='points.pickle')
parser.add_argument("-l", "--length", help="number of frames to record upon speeding detect", type=int, default=30)
parser.add_argument("-f", "--fps", help="framerate of video recording", default=20, type=int)
parser.add_argument("-n", "--number", help="number to divide vec quantity by", default=20, type=int)
parser.add_argument("-u", "--url", help="IP camera location url", type=str, default="cars.avi")
parser.add_argument("-c", "--camera", help="location of USB camera", type=int)
parser.add_argument("-d", "--debug", help="turn on debug mode", action="store_true")
parser.add_argument("-v", "--visual", help="turn on visual mode", action="store_true")
parser.add_argument("-r", "--record", help="enable recording", action="store_true")
parser.add_argument("-x", "--displacement", help="set minimum displacement", type=int, default=2)
parser.add_argument("--inf", help="Loop video infinitely", action="store_true")
parser.add_argument("-m", "--message", help="enable MQTT transmission", action="store_true")


args = parser.parse_args()

# select the project directory path
sep = "\\" if platform.system()=='Windows' else '/'
projDirList = path.realpath(__file__).split(sep)[0:-2]
projDir = sep.join(projDirList)

message = args.message

# number to divide number of vectors by
vecDiv = args.number

# Minimum displacement threshold
x_thresh = args.displacement

# loop over video infinitely
inf = args.inf

# ROI and dash input parameters
inputParams = args.input
# if just a filename without path, add to project path
if inputParams.count(sep) == 0:
    inputParams = projDir + sep + inputParams

# set variable values from options
recordLength = args.length
display = args.visual
# check if given URL or USB camera
if args.camera == None:
    dest = args.url
    # if just a filename without path, add to project path
    if dest.count(sep) == 0:
        dest = projDir + sep + dest
else:
    dest = args.camera

# recording frame rate
frameRate = args.fps
debug = args.debug
visual = args.visual
record = args.record
