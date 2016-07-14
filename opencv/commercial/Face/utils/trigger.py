import paho.mqtt.publish as mqtt
import json

'''
    {
        "event": "FaceDetect",
        "uri"  : "http://gateway/filename.avi",
        "facenum" : 4
        "timestamp" : Date.now()
        "offsetTime" :
    }

'''

def trigger(info):
    infoJSON = json.dumps(info)
    try:
        # print "sending off via MQTT" # works very fluidly
        mqtt.single("sensors/temperature/data", infoJSON, hostname="localhost")
    except:
        print "no MQTT connection found"
        pass
    print "Event triggered:", info["facenum"], "detected at frame:", info["offsetframe"],"!"
    return 1
