# Pluto Robot using the Romeo Board
## Overview
Pluto is a 2WD robot build using the *Romeo for Edison* breakout board by *DFRobot*.
The Romeo has a build in motor controller, allowing the motors to be directly connected to the board.
The robot runs a Flask server with a RESTful API, allowing the robot to be controlled remotely.
Users can both issue direct commands or create and run paths, where the robot follows a pre-programmed course.
## Getting started

### Set up
#### Software
Set up and update your Edison.
The robot scripts are written in Python **2.7**, so be sure that this is the version you're running.
In order to run the Flask server, we need to install the necessary packages.
This can be done by running
  **pip install flask flask-restful**

#### Wiring
Connect a 7.4v battery, motors with hall encoders, and button to the Romeo board as
shown in the diagram:
![alt text][diagram]
[diagram]: diagram.png "Romeo board connections"

## Controlling Pluto
Run the flask server using
  **python main.js**

Pluto is controlled through a RESTful API. Example requests can be found in the *postman*
commands, which can be imported into Postman.
### Motion Controls
Individual motions can be controlled by POSTing the necessary parameters in JSON format
to the route corresponding to the command.

#### Start the robot
**route:** */actions/start*
**parameters:** *none*
#### Stop the robot
**route:** */actions/stop*
**parameters:** *none*
#### Controlling individual wheels
**route:** */actions/wheels/<wheel_number>*
**parameters:** speed *(0-255)*
#### Driving the robot forward
**route:** */actions/forward*
**parameters:** speed *(0-255)*
#### Turning while driving
**route:** */actions/longturn*
**parameters:** th *(0-1)*, mag *(0-255)*
#### Performing a point turn
**route:** */actions/pointturn*
**parameters:** speed *(0-255)*

### Path Controls
Paths are sets of commands for the robot to take. They can be created, modified,
deleted, and executed.\
#### Managing Paths
##### GET
Retrieve the path. If no argument supplied, returns all available paths
##### POST
A path is sent as a JSON object containing an array of other JSON objects.
Each element in the array represents a command, and is supplied the necessary
arguments. For example:
```javascript
{
    "test1": [
        {
            "type": "start"
        },
        {
            "type": "forward",
            "speed": 253,
            "duration": 2
        },
        {
            "type": "pointTurn",
            "speed": 40,
            "duration": 0.5
        },
        {
            "type": "forward",
            "speed": 253,
            "duration": 1
        },
        {
            "type": "stop"
        }
    ]
}
```
##### DELETE
A path can be deleted by passing the path name as an argument into the request

#### Executing Paths
Paths can be executed by POSTing to the path's route. For example, POSTing to
**/paths/execute/test1** will execute the path named *test1*
