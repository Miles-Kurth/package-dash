# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       losanders6891                                                #
#   Created:      1/12/2026, 2:41:52 PM                                       #
#   Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
# from functools import singledispatch
import time

# Declare brain
brain = Brain()

# Declare motors
leftMotor = Motor(Ports.PORT1)
rightMotor = Motor(Ports.PORT10)
armMotor = Motor(Ports.PORT8)
clawMotor = Motor(Ports.PORT3)

# Declare sensors
gyro = Inertial(Ports.PORT11)

# Declare drivetrain
driveTrain = SmartDrive(leftMotor,rightMotor,gyro,319.19, 295, 40, MM, 1)


# Declare variables

xPos = 0
yPos = 0
heading = 0

positionSumList = []


# Functions

def printPositionList():
    global positionSumList, xPos, yPos
    for i in range(len(positionSumList)):
        print(positionSumList[i])

def printPosition():
    global positionSumList, xPos, yPos
    print("Current Position: ["+str(xPos)+", "+str(yPos)+"]")

def combineCoords(x, y):
    global positionSumList, xPos, yPos
    return [x, y]

def updatePosition():
    global positionSumList, xPos, yPos
    for i in range(len(positionSumList)):
        xPos += positionSumList[i][0]
        yPos += positionSumList[i][1]

# can take a single parameter [x,y]
def addMoveToList(coords):
    global positionSumList, xPos, yPos
    positionSumList.append(coords)

def turnToPoint(newCoords):
    global positionSumList, xPos, yPos
    print("Turning to point")
    x = newCoords[0]
    y = newCoords[1]
    dx = x - xPos
    dy = y - yPos
    heading = math.atan2(dy, dx)
    heading = math.degrees(heading)
    print("Heading: "+str(heading))
    # driveTrain.turn_to_heading(90)
    driveTrain.turn_for(RIGHT, 90, DEGREES)
    wait(100)

def moveToPoint(newCoords):
    global positionSumList, xPos, yPos
    print("Moving to point")
    addMoveToList(newCoords)
    turnToPoint(newCoords)
    x = newCoords[0]
    y = newCoords[1]
    dx = x - xPos
    dy = y - yPos
    distance = math.sqrt(dx**2 + dy**2)
    driveTrain.drive_for(FORWARD, distance, INCHES)
    updatePosition()
    wait(100)

def getHeading(newCoords):
    global positionSumList, xPos, yPos
    x = newCoords[0]
    y = newCoords[1]
    dx = x - xPos
    dy = y - yPos
    if (dx > 0):
        quadrant = 4
        if (dy > 0):
            quadrant = 1
    elif (dx < 0):
        quadrant = 2
        if (dy < 0):
            quadrant = 3
    math.atan2(dy, dx)

# Code below

brain.screen.print("Hello V5")
print("")

# addMoveToList([1,3])
# addMoveToList([5,8])
# addMoveToList([2,6])
# addMoveToList(combineCoords(4, 7))
# updatePosition()
# #should be [12, 24]

# printPositionList()

# printPosition()

# moveToPoint([-24,-36])
turnToPoint([-24, -36])






time.sleep(5)
print("PROGRAM ENDING")
