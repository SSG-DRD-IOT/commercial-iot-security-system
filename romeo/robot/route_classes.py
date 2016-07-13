###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: route_classes.py
# Project: Romeo Robot
# Description:
#   - this forms the Api - each class corresponds to a route
#   - class methods correspond to HTTP requests
# Last Modified: 7.13.2016
###############################################################################
from config import *
from controls import *

# drive individual wheels
class Wheels(Resource): # /actions/wheels/<wheel_number>
    def post(self, wheel_number):
        speed = request.json['speed']
        if wheel_number == 0:
            robot.driveRightWheel(speed)
        else:
            robot.driveLeftWheel(speed)
        return 'wheel spun!'

# drive both wheels at certain speed
class Forward(Resource): # /actions/forward
    def post(self):
        speed = request.json['speed']
        forward(robot, speed)
        return 'wheel'

# perform a long turn given th and mag
class LongTurn(Resource): # /actions/longturn
    def post(self):
        th = request.json['th']
        mag = request.json['mag']
        longTurn(robot, th, mag)
        return "long"

# perform a point turn
class PointTurn(Resource): # /actions/pointturn
    def post(self):
        speed = request.json['speed']
        pointTurn(robot, speed)
        return 'point'

# stop the robot (no parameters needed)
class Stop(Resource): # /actions/stop
    def post(self):
        robot.stop()
        return "stopped"

# start the robot (no parameters needed)
class Start(Resource): # /actions/start
    def post(self):
        robot.start()
        return "starting"

class Path(Resource): # /paths/administer/<path_name>, /paths/administer
    # GET request - return all paths available or specified path
    def get(self, **args):
        if len(args) == 0:
            return PATHS # returns all paths
        else:
            path_not_found(args['path_name']) # check if path exists
            return PATHS[args['path_name']] # respond with desired path
        return PATHS
    # POST request - create or update path
    def post(self):
        for path in request.json:
            PATHS[path] = request.json[path]
        return 'Path Appended'
    # DELETE request - remove path
    def delete(self, **args):
        if len(args) == 0:
            return 'Please select a path to delete'
        else:
            path_not_found(args['path_name'])
            del PATHS[args['path_name']]
            return 'Path '+ args['path_name'] + ' deleted!'

class ExecutePath(Resource): # /paths/execute/<path_name>
    # GET request - return path information
    def get(self, path_name):
        path_not_found(path_name)
        return PATHS[path_name]
    # POST request - execute the desired path
    def post(self, path_name):
        path_not_found(path_name)
        executePath(path_name)
        return path_name + " executed!"
