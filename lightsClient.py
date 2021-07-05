#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import datetime
from app import config
from fetch import Fetch
from phue import Bridge
from lights import Lights

# 3,6 - Hallway
# 1 - Desktop Bulb
# 2 - Living Room Bulb
# 4,5 - Bedroom

lights = Lights()

GPIO.setmode(GPIO.BCM)

# Declare defaults
motionSensorPin = 21
count = 0
inputMotionCount = 0
noMotionCount = 0
triggerNumber = 10
queueLightOff = 0

#Setup pins
GPIO.setup(motionSensorPin, GPIO.IN) #PIR

response = Fetch.get(config['API_URL'] + "/api/device/" + config['CLIENT_ID'] + "/")

def isWithinDoNotDisturb(start, end):
    splitStartTime = start.split(':')
    startTime = datetime.time(int(splitStartTime[0]), int(splitStartTime[1]), 0)

    splitEndTime = end.split(':')
    endTime = datetime.time(int(splitEndTime[0]), int(splitEndTime[1]), 0)

    return timeInRange(startTime, endTime, datetime.datetime.now().time())


def timeInRange(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

while True:
    if response["device_settings"]["light_feature"]:
        if (isWithinDoNotDisturb(response["device_settings"]["light_do_not_disturb_start"], response["device_settings"]["light_do_not_disturb_end"]) is False):
            # When motion is detected then do stuff
            if GPIO.input(motionSensorPin):
                print('motion detected, reset noMotionCount')
                print(inputMotionCount)
                # reset motion streak count
                noMotionCount = 0
                # Only turn on light if it hits the sensitivity_number and if lights turn on wasn't already executed. Don't want it running multiple times
                if (inputMotionCount is response["device_settings"]["sensitivity_number"] and queueLightOff is 0):
                    print('inputMotionCount hit count')
                    lights.turn_on([3,6])
                    time.sleep(response["device_settings"]["lights_on_seconds"])
                    queueLightOff = 1
                else:
                    inputMotionCount = inputMotionCount + 1
            else:
                print('no motion detected, reset inputMotionCount')
                # Reset motion streak count
                inputMotionCount = 0
                if queueLightOff:
                    print(noMotionCount)
                    print(response["device_settings"]["off_sensitivity_number"])
                    print(noMotionCount == response["device_settings"]["off_sensitivity_number"])
                    if (noMotionCount == response["device_settings"]["off_sensitivity_number"]):
                        print('turn off lights')

                        lights.turn_off([3,6])
                        queueLightOff = 0
                    else:
                        noMotionCount = noMotionCount + 1

    if(count % 500 is 1):
        response = Fetch.get(config['API_URL'] + "/api/device/" + config['CLIENT_ID'] + "/")

    count = count + 1
    time.sleep(0.2)
