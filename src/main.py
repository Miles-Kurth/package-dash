# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       losanders6891                                                #
#   Created:      1/12/2026, 2:41:52 PM                                        #
#   Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
import random

import urandom
from vex import *
# from functools import singledispatch
import time

# Declare brain
brain = Brain()

# Declare motors
leftMotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
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

def initializeRandomSeed():
    wait(100, MSEC)
    seed_val = (
        brain.battery.voltage(MV) 
        + brain.battery.current(CurrentUnits.AMP) * 100
        + brain.timer.system_high_res()
    )
    seed_val = seed_val**3
    urandom.seed(int(seed_val))
    temp = urandom.random() * seed_val
    urandom.seed(int(temp))
    print("Random seed: "+str(int(temp)))

def getRandomSign():
    return urandom.randint(0, 1) * 2 - 1

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
    heading = math.degrees(-heading)
    if heading < 0: heading = 360 + heading
    print("Target angle: "+str(heading))
    # if heading > 180: heading += 0.8
    # if heading < 180: heading -= 0.8
    # heading += 2
    # print("Target angle: "+str(heading if heading >= 0 else 360 + heading))
    # print("Current angle: "+str(gyro.heading()))
    driveTrain.turn_to_heading(heading)
    wait(100)
    print("Current angle after turn: "+str(gyro.heading()))

def moveToPoint(newCoords):
    global positionSumList, xPos, yPos
    print("//Moving to point: ["+str(newCoords[0])+", "+str(newCoords[1])+"]//")

    driveTrain.set_turn_velocity(20, PERCENT)
    driveTrain.set_turn_threshold(0.5)
    turnToPoint([newCoords[0], newCoords[1]])
    wait(100)
    driveTrain.set_turn_velocity(0.1, PERCENT)
    driveTrain.set_turn_threshold(0.1)
    turnToPoint([newCoords[0], newCoords[1]])

    wait(100)
    addMoveToList(newCoords)
    x = newCoords[0]
    y = newCoords[1]
    dx = x - xPos
    dy = y - yPos
    distance = math.sqrt(dx**2 + dy**2)
    driveTrain.drive_for(FORWARD, distance, INCHES)
    updatePosition()
    wait(100)
    print("Current angle after move: "+str(gyro.heading()))

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

# to do
def getCoordsFromHeading(heading, distance):
    global positionSumList, xPos, yPos
    x = distance * math.cos(math.radians(heading))
    y = distance * math.sin(math.radians(heading))
    return [x, y]



# Code below

brain.screen.print("Hello V5")
print("")

gyro.calibrate()
while gyro.is_calibrating():
    wait(50)

driveTrain.set_drive_velocity(25, PERCENT)
driveTrain.set_turn_velocity(10, PERCENT)
driveTrain.set_turn_threshold(0.5)


# addMoveToList([1,3])
# addMoveToList([5,8])
# addMoveToList([2,6])
# addMoveToList(combineCoords(4, 7))
# updatePosition()
# #should be [12, 24]

# printPositionList()

# printPosition()





initializeRandomSeed()



h = urandom.randint(0, 36) * getRandomSign()
k = urandom.randint(0, 36) * getRandomSign()

# print("Random point: ["+str(h)+", "+str(k)+"]")


# moveToPoint([h, k])

# printPosition()

moveToPoint([-60, -24])
printPosition()
moveToPoint([-96, -72])
printPosition()





time.sleep(5)
print("PROGRAM ENDING")
