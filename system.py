#!/usr/bin/env python

import datetime
import time
import os
import RPi.GPIO as GPIO
import picamera

ON = 0
OFF = 1
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)
prevSoap = 1
soap = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)
prevWater = OFF
water = OFF

waterOn = False
soapOn = False
recordCount = 0
timeCount = 0
soapCount = 0
debounceTime = 0

def checkPath():
    currentDatePath = "/home/pi/Documents/Data/" + datetime.datetime.now().strftime("%m_%d_%Y")
    if(os.path.exists(currentDatePath) is True):
        return True
    else:
        os.mkdir(currentDatePath)
        return False
    
while 1:
    water = GPIO.input(5)
    soap = GPIO.input(6)

    # Water Sensor
    if(prevWater == OFF and water == ON):
        waterOn = True
        
    if(prevWater == ON and water == OFF):
        waterOn = False
        
    prevWater = water
    
    #Soap Sensor Logic
    if(prevSoap == OFF and soap == ON and time.time() > debounceTime + 1):
        soapOn = True
        soapCount = soapCount + 1
        debounceTime = time.time()

        
    if(prevSoap == ON and soap == OFF):
        soapOn = False
        
    prevSoap = soap
         
    # Recording Logic
    if((waterOn is True) and recordCount == 0):
        if(waterOn is True):
            checkPath()
            print("Water Sensor On")
        timeCount = time.time();
        recordCount = 1
        camera.start_recording(date + '.h264')
        filename = date + '.h264'
        
        
    if((waterOn is False) and (recordCount == 1) and (time.time() > timeCount + 10)):
        camera.stop_recording()
        savePath = "/home/pi/Documents/Data/" + datetime.datetime.now().strftime("%m_%d_%Y")
        completeVideo = os.path.join(savePath, filename)
        print("Water Sensor Stopped")
        recordCount = 0
        prevSoap = OFF
        soap = OFF
        water = OFF
        prevWater = OFF
        timeCount = 0
        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        print("Soap Count: ")
        print(soapCount);
        continue

print("Camera Done")
print("Soap Count: ")
print(soapCount);
        


