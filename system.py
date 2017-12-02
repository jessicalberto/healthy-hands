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


while 1:
    water = GPIO.input(5)
    soap = GPIO.input(6)

    # Water Sensor
    if(prevWater == OFF and water == ON):
        print("Water Detected")
        waterOn = True
        
    if(prevWater == ON and water == OFF):
        print("Water Stopped")
        waterOn = False
        
    prevWater = water
    
    #Soap Sensor
    if(prevSoap == OFF and soap == ON):
        print("Soap Start")

        soapOn = True

        
    if(prevSoap == ON and soap == OFF):
        print("Soap Stopped")
        soapOn = False
        
    prevSoap = soap
    
    # Recording Logic
    if((waterOn is True or soapOn is True) and recordCount == 0):
        print("Start")
        recordCount = 1
        camera.start_recording(date + '.h264')
        
    if((waterOn is False and soapOn is False) and recordCount == 1):
        camera.stop_recording()
        print("Stop Recording")
        recordCount = 0
        prevSoap = OFF
        soap = OFF
        water = OFF
        prevWater = OFF
        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        continue

print("Camera Done")
        
##camera.start_recording(filename)
##sleep(5)
##camera.stop_recording()
##completed_video = os.path(save_path, filename)

##camera.start_recording('my_video.h264')
##camera.wait_recording(60)
##camera.stop_recording()


