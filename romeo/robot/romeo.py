###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: romeo.py
# Project: Romeo Robot
# Description:
#   Low-level controls for Romeo robot
# Last Modified: 7.13.2016
###############################################################################
import mraa

class Romeo():
    """ Class for controlling the DFRobot Romeo for Edison
    To drive motors, use ADC, PWM, etc., interface with AtMega8 board
    byte array format:
    ( 0x55, 0xaa, 0x[cmd][x], 0x[arg] )
    """
    # encoder counters
    lCount = 0
    rCount = 0
    def __init__(self):
        # set up I2C
        self.i2c = mraa.I2c(1)
        self.i2c.frequency(100000)
        self.i2c.address(0x04)

        self.leftWheelSpeed = 0
        self.rightWheelSpeed = 0
        self.leftWheelDirection = 0
        self.rightWheelDirection = 0
        self.stopped = False

        # Motor corrections in range (0, 1)
        self.L_CORRECTION = 1
        self.R_CORRECTION = .888

    ## Encoder Counter Controls
    def leftReset(self):
        self.lCount = 0
    def rightReset(self):
        self.rCount = 0
    # signs change to correspond to encoder orientation
    def leftIncr(self, pos):
        if pos:
            self.lCount -= 1
        else:
            self.lCount += 1
    def rightIncr(self, pos):
        if pos:
            self.rCount += 1
        else:
            self.rCount -= 1
    # retrieve encoder counts
    def getLCount(self):
        return self.lCount
    def getRCount(self):
        return self.rCount

    ## Wheel Controls ##
    # set the wheel directions
    def setLeftWheel(self, direction):
        "0-->CW; 1-->CCW"
        direction = direction & 0xFF
        self.sendI2C(bytearray([0x55, 0xaa, 0xB1, direction]))
        self.leftWheelDirection = direction
    def setRightWheel(self, direction):
        "0-->CW; 1-->CCW"
        direction = direction & 0xFF
        self.sendI2C(bytearray([0x55, 0xaa, 0xB2, direction]))
        self.rightWheelDirection = direction

    # drive the wheels with a given PWM speed
    def driveLeftWheel(self, speed):
        "speed is in [0, 255]"
        if (speed > 0) != (self.leftWheelDirection > 0):
            self.setLeftWheel(not self.leftWheelDirection)
        speed = abs(int(round(self.L_CORRECTION * speed))) & 0xFF
        self.sendI2C(bytearray([0x55, 0xaa, 0xC1, speed]))
        self.leftWheelSpeed = speed
    def driveRightWheel(self, speed):
        "speed is in [0, 255]"
        if (speed > 0) != (self.rightWheelDirection > 0):
            self.setRightWheel(not self.rightWheelDirection)
        speed = abs(int(round(R_CORRECTION * speed))) & 0xFF
        self.sendI2C(bytearray([0x55, 0xaa, 0xC2, speed]))
        self.rightWheelSpeed = speed
    # stop the robot
    def stop(self):
        self.sendI2C(bytearray([0x55, 0xaa, 0xC1, 0]))
        self.sendI2C(bytearray([0x55, 0xaa, 0xC2, 0]))
        self.stopped = True
    # start the robot
    def start(self):
        self.stopped = False

    ## I2C Send ##
    # necessary for controlling motor driver
    def sendI2C(self, cmd):
        cmd.append(sum(cmd)&0xFF)
        self.i2c.write(cmd)
