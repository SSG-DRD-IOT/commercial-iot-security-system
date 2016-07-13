###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: conv.py
# Project: Romeo Robot
# Description:
#   useful conversion macros
#   convert distance <-> ticks <-> rotation angle
# Last Modified: 7.13.2016
###############################################################################

"""Module of Spacial, Angular, and Tick conversions macros"""
# Number of ticks is int
# Distance in Meters
# Angle in Radians

import math

DIAM = .042 # 42 mm wheels
TPR = 70 # number of ticks per revolution on encoder
AXWID = .09 # axle width; distance between wheel centers

### Spacial <-> Ticks
# convert from distance to number of edges
def dist2tick(dist):
    ticks = dist * TPR / (math.pi * DIAM)
    return ticks

# convert number of edges to distance
def tick2dist(tick):
    dist = DIAM * math.pi * tick / TPR
    return dist

### Rotation <-> Ticks
## single wheel rotation
# radians to edges
def ang2tick_s(ang):
    ticks = dist2tick(ang * AXWID)
    return ticks
# edges to radians
def tick2ang_s(ticks):
    ang = ticks2dist(ticks) / AXWID
    return ang

## point rotation
# radians to edges
def ang2tick_p(ang):
    ticks = dist2tick(ang * AXWID/2)
    return ticks
# edges to radians
def tick2ang_p(ticks):
    ang = ticks2dist(ticks) / (AXWID/2)
    return ang
