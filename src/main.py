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
camera_RedPipe = Colordesc(3, 151, 6, 3, 10, 0.35)

# Declare sensors
gyro = Inertial(Ports.PORT11)
camera = AiVision(Ports.PORT15, camera_RedPipe)

# Declare drivetrain
driveTrain = SmartDrive(leftMotor,rightMotor,gyro,319.19, 295, 40, MM, 1)


# Declare variables

xPos = 8
yPos = 6
targetDistance = 0

distanceConstant = 375

positionList = [] #list of all points the robot has traveled to


# Functions

# Prints a funny message to the brain screen
def printFunnyMessage():
    wordList = ["Dash", "Pack"]
    suffixList = ["age", "ing", ""]
    determinerList = ["the", "a", "this", "that"]
    wordOrderList = ["1D2", "D12", "12D"]

    word1 = wordList[int(urandom.random() * 2)]
    word2 = wordList[int(urandom.random() * 2)].lower()

    if (word1 == "Dash"): #prevent "dashage" in word 1
        suffix1 = suffixList[int(urandom.random() * 2) + 1]
    else:
        suffix1 = suffixList[int(urandom.random() * 3)]
    
    if (word2.lower() == "dash"): #prevent "dashage" in word 2
        suffix2 = suffixList[int(urandom.random() * 2) + 1]
    else:
        suffix2 = suffixList[int(urandom.random() * 3)]

    det = determinerList[int(urandom.random() * 4)]

    if (det == "this" or det == "that"): #only allow pattern 3 if det is this or that
        wordOrder = wordOrderList[int(urandom.random() * 3)]
    else:
        wordOrder = wordOrderList[int(urandom.random() * 2)]

    if (wordOrder == "1D2"):
        brain.screen.print(word1 + suffix1 + " " + det + " " + word2 + suffix2 + "!")
    elif (wordOrder == "D12"):
        brain.screen.print(det + " " + word1 + suffix1 + " " + word2 + suffix2 + "!")
    elif (wordOrder == "12D"):
        brain.screen.print(word1 + suffix1 + " " + word2 + suffix2 + " " + det + "!")
    
    print("")

# All setup code goes here
def setup():
    gyro.calibrate()
    driveTrain.set_drive_velocity(25, PERCENT)
    armMotor.set_position(0,DEGREES)
    armMotor.spin_for(FORWARD,230,DEGREES) #"neutral" height, from floor
    clawMotor.spin_for(FORWARD, 2, SECONDS) #full open
    while gyro.is_calibrating():
        wait(50)

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
    # temp = pow(urandom.random(), seed_val)
    # urandom.seed(int(temp))
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
    # print("Turning to point")
    x = newCoords[0]
    y = newCoords[1]
    dx = x - xPos
    dy = y - yPos
    heading = math.atan2(dy, dx)
    heading = math.degrees(-heading)
    if heading < 0: heading = 360 + heading
    # print("Target angle: "+str(heading))
    driveTrain.turn_to_heading(heading)
    wait(100)
    # print("Current angle after turn: "+str(gyro.heading()))

# Moves the robot to [x, y]
def moveToPoint(newCoords):
    global positionList, xPos, yPos
    # print("//Moving to point: ["+str(newCoords[0])+", "+str(newCoords[1])+"]//")
    driveTrain.set_turn_velocity(20, PERCENT)
    driveTrain.set_turn_threshold(0.5)
    turnToPoint([newCoords[0], newCoords[1]])
    driveTrain.set_turn_velocity(0.1, PERCENT)
    driveTrain.set_turn_threshold(0.1)
    turnToPoint([newCoords[0], newCoords[1]])
    driveTrain.set_turn_velocity(5, PERCENT)
    driveTrain.set_turn_threshold(0.5)

    addMoveToList(newCoords)
    x = newCoords[0] #start math
    y = newCoords[1]
    dx = x - xPos
    dy = y - yPos
    distance = math.sqrt(dx**2 + dy**2)
    driveTrain.drive_for(FORWARD, distance, INCHES)
    updatePosition()
    wait(100)
    # print("Current angle after move: "+str(gyro.heading()))
    initializeRandomSeed()

# Returns the coordinates [x, y] of an object when given a heading and distance
def getCoordsFromHeading(heading, distance):
    global positionList, xPos, yPos
    x = xPos + ( distance * math.cos(math.radians(heading)) )
    y = yPos + ( distance * math.sin(math.radians(heading)) )
    return [x, y]

# Goes to the pipe and picks it up
def pickUpPipe():
    global positionList, xPos, yPos, targetDistance, distanceConstant

    driveTrain.turn_to_heading(gyro.heading() + getPipeAngle()*0.7)
    driveTrain.drive_for(FORWARD, getPipeDistance() - 1, INCHES)
    addMoveToList( getCoordsFromHeading(gyro.heading(), getPipeDistance() - 1) )
    updatePosition()

    clawMotor.spin_for(REVERSE, 1, SECONDS)
    armMotor.spin_for(FORWARD, 40, DEGREES)

# Returns the angle to the pipe, in degrees
def getPipeAngle():
    global positionList, xPos, yPos, targetDistance, distanceConstant

    canOffsetSum = 0
    for i in range(30):
        camera.take_snapshot(camera_RedPipe)
        obj = camera.largest_object()
        hOffset = obj.centerX - 160
        canOffsetSum += hOffset
    hOffset = canOffsetSum / 30

    angle = hOffset * (74 / 320)
    print("hOffset: "+str(hOffset))
    print("angle: "+str(angle))

    return angle

# Returns the distance to the pipe, in inches
def getPipeDistance():
    global positionList, xPos, yPos, targetDistance, distanceConstant

    largest = 0
    for i in range(30):
        camera.take_snapshot(camera_RedPipe)
        obj = camera.largest_object()
        objWidth = obj.width
        if (objWidth > largest):
            largest = objWidth

    objDist = (distanceConstant / largest)
    print("objWidth: "+str(largest))
    print( "Distance: "+str(objDist) )

    return objDist

# Drops the pipe in place and returns arm to neutral position
def dropPipe():
    clawMotor.spin_for(FORWARD, 1, SECONDS)
    armMotor.spin_for(REVERSE, 40, DEGREES)
    

#//--------------->>/ MILES COORDINATE END /<<---------------//



# Code below

initializeRandomSeed()

printFunnyMessage()

setup() #ALL SETUP CODE GOES HERE



moveToPoint([50, 12])
pickUpPipe()

# moveToPoint([40, 12])

moveToPoint([72,120])

moveToPoint([120, 126]) #WIP (may need to move forward)
dropPipe()

##ADD NEGATIVE OFFSET

# moveToPoint([58, 132])
# turnToPoint([36, 132])
# pickUpPipe()

# moveToPoint([120, 126]) #WIP (may need to move forward)
# dropPipe()





#.  moveToPoint([, ])

print("END OF CODE")
time.sleep(5)
print("PROGRAM ENDING")
