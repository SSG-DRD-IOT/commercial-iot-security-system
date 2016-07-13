###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: config.py
# Project: Romeo Robot
# Description:
#   - imports Flask and Flask_restful packages
#   - Instantiates the Romeo robot
#   - Creates a test path
# Last Modified: 7.13.2016
###############################################################################

from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from romeo import Romeo

# instantiate robot
robot = Romeo()

# create a test path
PATHS = {
    "test": [ # a path is an array of dicts
        {
            "type": "start"
        },
        {
            "type": "forward", # commands contain necessary parameters
            "speed": 253,
            "duration": 2
        },
        {
            "type": "stop"
        }
    ]
}

def path_not_found(path_name): # returns 404 when invalid path
    if path_name not in PATHS:
        abort(404, message="Path {} doesn't exist".format(path_name))
