#!/usr/bin/env python3

'''
	This file trains drone to do backflip

	Author: Steven Warner
'''


import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw, Attitude)
import random

# public variables
global height
global angle
global angleIncrement
global rightRollCount

height = 0
rightRollCount = 0
leftRollTag = "L"
rightRollTag = "R"
sizeOfThoughtPattern = 25
maxHeight = 10
angle = 0
angleIncrement = 10
delay = 0.2

# makes thought pattern
def makeThought():
    # variable creation
    pattern = ""
    # randomly adds moves to pattern
    for i in range(sizeOfThoughtPattern):
        # adds random right or left
        if (random.random() < 0.5):
            pattern += rightRollTag
        else:
            pattern += leftRollTag

    # returns pattern
    return pattern

# fitness function
def fitFunction():
    # gets roll count
    fit = rollCount

    # decrements for each meter above threshold
    while (height > 10):
        fit /= 2.0
        height /= 4

    # returns fit
    return fit

# roll right
async def rollRight(drone):
    # sets variables
    global angle, rightRollCount

    # roll operation
    angle += angleIncrement
    attitude = Attitude(roll_deg=angle,pitch_deg=0.0,yaw_deg=0.0,thrust_value=7.0)
    await drone.offboard.set_attitude(attitude)
    await asyncio.sleep(delay)

    # increments roll count
    rightRollCount += 1

# roll left
async def rollLeft(drone):
    # makes angle public
    global angle

    # roll operation
    angle -= angleIncrement
    attitude = Attitude(roll_deg=angle,pitch_deg=0.0,yaw_deg=0.0,thrust_value=7.0)
    await drone.offboard.set_attitude(attitude)
    await asyncio.sleep(delay)

# runs drone based on thought pattern
async def runDrone():
    # variable creation
    drone = System()

    # sets up drone
    await drone.connect(system_address="udp://14540")
    async for state in drone.core.connection_state():
        if (state.is_connected):
            print(f"-- connected to drone")
            break

    async for health in drone.telemetry.health():
        if (health.is_global_position_ok and health.is_home_position_ok):
            print(f"-- global position estimated ok")
            break

    await drone.action.arm()
    await drone.offboard.set_position_ned(PositionNedYaw(0.0,0.0,-90.0,0.0))

    # sets up thoughts
    # moves drone to thoughts 
    # takes fittness function
    # saves to file if good
    # lands drone
# driver
def run():
    print(makeThought())
    asyncio.run(runDrone())
run()
