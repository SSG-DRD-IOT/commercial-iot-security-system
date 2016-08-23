###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: trigger.py
# Project: Security System
# Description:
#   trigger function
#       when event is triggered, send data in JSON format by MQTT
# Last Modified: 7.14.2016
###############################################################################
import paho.mqtt.publish as mqtt
import json
from args import message

def trigger(info):
    # global message
    # convert dict into JSON object
    infoJSON = json.dumps(info)
    if message:
        try:
            mqtt.single("sensors/video/motion", infoJSON, hostname="localhost") # blocks up application
            # print "hi"
        except:
            print "no MQTT connection found"
            pass
    print "Event triggered:", info["event"],"!"
    return 1
