import time
import sys
import paho.mqtt.publish as mqtt


'''
    {
        "event": "FaceDetect",
        "uri"  : "http://gateway/filename.avi",
        "facenum" : 4
        "timestamp" : Date.now()
        "offsetTime" : 
    }

'''

def trigger(number):
    mqtt.single("sensors/temperature/data", "I see a face", hostname="localhost")
    print "Event triggered:", number, "detected!"
    return 1
