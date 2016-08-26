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
# Last Modified: 7.18.2016
###############################################################################
import paho.mqtt.publish as mqtt
import json
import args
''' General format of JSON:
    {
        "event": "FaceDetect",
        "uri"  : "http://gateway/filename.avi",
        "facenum" : 4
        "timestamp" : Date.now()
        "offsetframe" : 100
    }

'''

def trigger(info):
    # convert dict into JSON object
    infoJSON = json.dumps(info)
    if args.message:
        try:
            mqtt.single("sensors/video/face", infoJSON, hostname="localhost") # blocks up application
        except:
            print "no MQTT connection found"
            pass
    print "Event triggered:", info["event"]
    print info
    return 1
