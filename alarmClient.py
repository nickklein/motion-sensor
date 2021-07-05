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

#Declare defaults
motionSensorPin = 21
soundPin = 20
count = 0
motionCount = 0

#Init Pins
GPIO.setup(motionSensorPin, GPIO.IN) #PIR
GPIO.setup(soundPin, GPIO.OUT) #PIR

response = Fetch.get(config['API_URL'] + "/api/device/" + config['CLIENT_ID'] + "/")

def isWithinSoundAlarmTime(start, end):
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
    if response["device_settings"]["alarm_feature"]:
        if (response["device_settings"]["alarm_on"]):
            # When motion is detected then do stuff
            if GPIO.input(motionSensorPin):
                print('sms: motion detected')

                if (motionCount is response["device_settings"]["alarm_sensitivity"]):
                    print('sens triggered')
                    data = {
                        'device_id': config['CLIENT_ID'], 
                    }
                    postResponse = Fetch.post(config['API_URL'] + "/api/notify/send", {}, data)
                    time.sleep(60)
                    print('after sleep')
                else:
                    motionCount = motionCount + 1
            else:
                motionCount = 0
        if (isWithinSoundAlarmTime(response["device_settings"]["sound_start"], response["device_settings"]["sound_end"])):
            if (response["device_settings"]["sound_alarm"]):
                if GPIO.input(motionSensorPin):
                    print('sound: motion detected')
                    if (motionCount is response["device_settings"]["sound_sensitivity"]):
                        GPIO.output(soundPin, GPIO.HIGH)
                        time.sleep(1)
                        GPIO.output(soundPin, GPIO.LOW)
                        time.sleep(60)
                    else:
                        motionCount = motionCount + 1
                else:
                    motionCount = 0




    if(count % 500 is 1):
        response = Fetch.get(config['API_URL'] + "/api/device/" + config['CLIENT_ID'] + "/")

    count = count + 1
    time.sleep(0.2)
