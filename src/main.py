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
import time

# Declare brain
brain = Brain()

# Declare motors
leftMotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
armMotor = Motor(Ports.PORT8,  GearSetting.RATIO_36_1, False)
clawMotor = Motor(Ports.PORT3 , GearSetting.RATIO_36_1, False)

clawMotor.set_stopping(HOLD)
armMotor.set_stopping(HOLD)

# AI Vision color descriptions
camera_BluePipe = Colordesc(1, 11, 54, 134, 10, 0.2)
camera_RedPipe = Colordesc(3, 166, 26, 28, 10, 0.77)

# Declare sensors
gyro = Inertial(Ports.PORT11)
camera = AiVision(Ports.PORT15, camera_RedPipe)

# Declare drivetrain
driveTrain = SmartDrive(leftMotor,rightMotor,gyro,319.19, 295, 40, MM, 1)


# Declare variables

xPos = 8
yPos = 6
# heading = 0

positionList = [] #list of all points the robot has traveled to


# Functions

#//---------------<</ MILES COORDINATE START />>---------------//
#                       // DO NOT TOUCH //

# Sets the seed for random events
def initializeRandomSeed():
    seed_val = (
        brain.battery.voltage(MV) 
        + brain.battery.current(CurrentUnits.AMP) * 100
        + brain.timer.system_high_res()
    )
    seed_val = seed_val**3
    urandom.seed(int(seed_val))
    temp = pow(urandom.random(), seed_val)
    urandom.seed(int(temp))
    # print("Random seed: "+str(int(temp)))

# Picks randomly either 1 or -1
def getRandomSign():
    return urandom.randint(0, 1) * 2 - 1

# Prints positionList
def printPositionList():
    global positionList, xPos, yPos
    for coordPair in positionList:
        print(coordPair)

# Prints the robot's current position to the console
def printPosition():
    global positionList, xPos, yPos
    print("Current Position: ["+str(xPos)+", "+str(yPos)+"]") # example: "Current Position: [-36, -60]"

# Updates xPos and yPos to match the most recent move in positionList
def updatePosition():
    global positionList, xPos, yPos
    xPos = positionList[len(positionList) - 1][0]
    yPos = positionList[len(positionList) - 1][1]

# Adds [x, y] to the position list
def addMoveToList(coords):
    global positionList, xPos, yPos
    positionList.append(coords)

# Turns the robot to face [x, y]
def turnToPoint(newCoords):
    global positionList, xPos, yPos
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

# Moves the robot to [x, y]
def moveToPoint(newCoords):
    global positionList, xPos, yPos
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
    x = newCoords[0] #start math
    y = newCoords[1]
    dx = x - xPos
    dy = y - yPos
    distance = math.sqrt(dx**2 + dy**2)
    driveTrain.drive_for(FORWARD, distance, INCHES)
    updatePosition()
    wait(100)
    print("Current angle after move: "+str(gyro.heading()))
    initializeRandomSeed()

# Returns the coordinates [x, y] of an object when given a heading and distance
def getCoordsFromHeading(heading, distance):
    global positionList, xPos, yPos
    x = distance * math.cos(math.radians(heading))
    y = distance * math.sin(math.radians(heading))
    return [x, y]

def getPipeCoords():
    global positionList, xPos, yPos
    heading = gyro.heading()
    camPosX = math.cos(math.radians(gyro.heading())) * 7.5
    camPosY = math.sin(math.radians(gyro.heading())) * 7.5

    distanceConstant = 14.1732  #1.1811*12

    camera.take_snapshot(camera_RedPipe)
    obj = camera.largest_object()
    objX = obj.centerX
    objY = obj.centerY
    objWidth = obj.width
    objDist = distanceConstant / objWidth

    hOffset = objX - 160
    print("hOffset: "+str(hOffset))
    
    # return coords

#//--------------->>/ MILES COORDINATE END /<<---------------//


# Code below

brain.screen.print("Dashing the package")
print("")

initializeRandomSeed()

gyro.calibrate()
while gyro.is_calibrating():
    wait(50)

driveTrain.set_drive_velocity(25, PERCENT)


armMotor.set_position(0,DEGREES)
armMotor.spin_for(FORWARD,210,DEGREES)

getPipeCoords()

# moveToPoint([60, 12])
# printPosition()
# moveToPoint([30, 12])
# printPosition()
# moveToPoint([60,84])
# moveToPoint([125, 125])
# printPosition()



print("END OF CODE")
time.sleep(5)
print("PROGRAM ENDING")
