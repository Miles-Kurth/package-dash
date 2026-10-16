# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       losanders6891                                                #
#   Created:      10/12/2026, 2:41:52 PM                                       #
#   Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
from functools import singledispatch

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

def combineCoords(x, y):
    global positionSumList, xPos, yPos
    return [x, y]

def turnToPoint():
    global positionSumList, xPos, yPos
    pass

def updateList():
    global positionSumList, xPos, yPos
    for i in range(len(positionSumList)):
        xPos += positionSumList[i][0]
        yPos += positionSumList[i][1]

def printList():
    global positionSumList, xPos, yPos
    for i in range(len(positionSumList)):
        print(positionSumList[i])

# def addMoveToList(distX, distY):
#     positionSumList.append([distX, distY])

def addMoveToList(*args):
    # Case 1: A single array/list was passed
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        data = args[0]
        print(f"Received an array of length {len(data)}: {data}")
        
    # Case 2: Two individual integers were passed
    elif len(args) == 2 and all(isinstance(x, int) for x in args):
        int1, int2 = args
        print(f"Received two integers: {int1} and {int2}")
        
    else:
        raise ValueError("Function expects either a single list or two integers.")

def turnToPoint():
    pass

def moveToPoint():
    pass


# Code below

brain.screen.print("Hello V5")
print("")

addMoveToList(1,3)
addMoveToList(5,8)
addMoveToList(2,6)
updateList()
#should be [8, 17]

printList()










wait(5000)
print("PROGRAM ENDING")
