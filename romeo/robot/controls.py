###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: controls.py
# Project: Romeo Robot
# Description:
#   Higher layer of Romeo motion controls
#   - Dynamic movements contain no feedback mechanism
#   - Measured movements take in encoder inputs
#
# Last Modified: 7.13.2016
###############################################################################

# import romeo
from time import sleep
from config import *
from conv import *
import mraa, time

# Define Interrupt Pins
L_A_PIN = 47 # D8
L_B_PIN = 21 # D9
R_A_PIN = 51 # D10
R_B_PIN = 38 # D11

STOP_BTN = 37 # D13

# Set up Interrupt Pins
phLA = mraa.Gpio(L_A_PIN)
phLB = mraa.Gpio(L_B_PIN)
phRA = mraa.Gpio(R_A_PIN)
phRB = mraa.Gpio(R_B_PIN)
btnPin = mraa.Gpio(STOP_BTN)

# set interrupt pin directions
phLA.dir(mraa.DIR_IN)
phLB.dir(mraa.DIR_IN)
phRA.dir(mraa.DIR_IN)
phRB.dir(mraa.DIR_IN)
btnPin.dir(mraa.DIR_IN)

# reset counters before performing new measured move
def resetCounters(robot):
    robot.leftReset()
    robot.rightReset()
# Interrupt Routines
def lCounter(robot):
    if phLB.read():
        robot.leftIncr(True)
    else:
        robot.leftIncr(False)
def rCounter(robot):
    if phRB.read():
        robot.rightIncr(True)
    else:
        robot.rightIncr(False)

### Dynamic Controls

# drive both wheels in same direction
def forward(robot, speed):
    robot.driveLeftWheel(speed)
    robot.driveRightWheel(speed)

# roll robot in certain direction
def longTurn(robot, th, mult):
    "th in [0, 1] is right_pwr/net_pwr; neg -> cw, pos -> ccw"
    # th controls the offset between the wheels
    robot.driveRightWheel(int(round(th * mult)))
    robot.driveLeftWheel(int(round((1-th) * mult)))

# perform an in-place point turn
def pointTurn(robot, speed):
    robot.driveRightWheel(speed) # wheels turn in opposite directions
    robot.driveLeftWheel(-speed)

### Measured (Encoder-based) Controls
# in-place turn using a single wheel
def singleTurn(robot, th, speed):
    # th given in radians
    resetCounters(robot)
    if th > 0: # set which wheel to drive and corresponding interrupt pin
        driveWheel, counter, iPin = robot.driveRightWheel, \
            robot.getRCount, phRA
        iPin.isr(mraa.EDGE_RISING, lCounter, robot)
    else:
        driveWheel, counter, iPin = robot.driveLeftWheel, \
            robot.getLCount, phLA
        iPin.isr(mraa.EDGE_RISING, rCounter, robot)
    driveWheel(speed)
    while ( abs(counter()) < abs(ang2tick_s(th)) ):
        # if btnPin.read(): # if button attached
        #     break # stop robot on buttonpress
        continue
    robot.stop()
    iPin.isrExit()
    print counter()
    return

# point turn for a specific angle
def pointTurnM(robot, angle, speed):
    resetCounters(robot)
    # set forward and reverse wheels and their corresponding interrupts
    if angle > 0:
        fWheel, rWheel, count1, count2, fInt, rInt = robot.driveRightWheel, \
            robot.driveLeftWheel, robot.getRCount, robot.getLCount, \
            phRA, phLA
        counter1 = rCounter
        counter2 = lCounter
    else:
        fWheel, rWheel, count1, count2, fInt, rInt = robot.driveLeftWheel, \
            robot.driveRightWheel, robot.getLCount, robot.getRCount, \
            phLA, phRA
        counter1 = lCounter
        counter2 = rCounter
    fInt.isr(mraa.EDGE_RISING, counter1, robot)
    rInt.isr(mraa.EDGE_RISING, counter2, robot)
    fWheel(speed)
    rWheel(-speed)
    # keep driving while number of ticks spun does not exceed ticks required for angle
    while abs( count1() ) < abs( ang2tick_s( angle ) ):
        print count1(), "|", count2()
        continue
    robot.stop()
    fInt.isrExit()
    rInt.isrExit()
    return

# use to manually find number of ticks detected in encoder revolution
def calibrateTicks(robot, wheel, spd):
    resetCounters(robot)
    if wheel:
        driveWheel, countWheel, intWheel, counter = robot.driveRightWheel, \
            robot.getRCount, phRA, rCounter
    else:
        driveWheel, countWheel, intWheel, counter = robot.driveLeftWheel, \
        robot.getLCount, phLA, lCounter
    intWheel.isr(mraa.EDGE_RISING, counter, robot)
    driveWheel(spd)
    raw_input("Press ENTER when one cycle completed") # will output number of ticks
    robot.stop()
    intWheel.isrExit()
    print(countWheel())
    return countWheel()

# drive forward for specific distance
def forwardDist(robot, dist, speed):
    resetCounters(robot)
    # calculate number of encoder edges corresponding to distance
    dTicks = dist2tick(dist)
    phLA.isr(mraa.EDGE_RISING, lCounter, robot)
    phRA.isr(mraa.EDGE_RISING, rCounter, robot)
    while (robot.getLCount() < dTicks) and (robot.getRCount < dTicks):
        forward(robot, speed)
    robot.stop()
    phLA.isrExit()
    phRA.isrExit()
    return

# execute path command-by-command
def executePath(path_name):
    for cmd in PATHS[path_name]: # cmd is a dict
        cmdType = cmd['type']
        if cmdType == 'stop':
            robot.stop()
            print 'stopped'
            continue
        elif cmdType == 'start':
            robot.start()
            print 'started'
            continue
        elif cmdType == 'forward':
            forward(robot, cmd['speed'])
            print 'forward', cmd['speed']
        elif cmdType == 'leftWheel':
            robot.driveLeftWheel(cmd['speed'])
            print 'left', cmd['speed']
        elif cmdType == 'rightWheel':
            robot.driveRightWheel(cmd['speed'])
            print 'right', cmd['speed']
        elif cmdType == 'longTurn':
            longTurn(robot, cmd['th'], cmd['mag'])
            print 'long turn', 'th: ',float(cmd['th']) / 100, 'mag: ', cmd['mag']
        elif cmdType == 'pointTurn':
            pointTurn(robot, cmd['speed'])
            print 'point turn', cmd['speed']
        sleep(cmd['duration'])
    return 1
