###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: dtinfo.py
# Project: Security System
# Description:
#   macros for supplying strings with date and time information
# Last Modified: 7.14.2016
###############################################################################
import time

# current date
def currDate(): # day-month-year
    return time.strftime("%d-%m-%Y")
current time
def currTime(): # hours-minutes-seconds
    return time.strftime("%H-%M-%S")
