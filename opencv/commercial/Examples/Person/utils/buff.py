###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: genBuffMask.py
# Project: Security System
# Description:
#   generate a buffer mask consisting of continuous binary ones
# Last Modified: 7.14.2016
###############################################################################
def genBuffMask(bufferFrames):
    'create bitwise mask for buffer length'
    # buffmask = 0...01...(n)...1
    buffMask = (2**bufferFrames) - 1
    return buffMask
