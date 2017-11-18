#!/usr/bin/env python

import datetime
import time
import os
import RPi.GPIO as GPIO
import picamera

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
prevState = 1
state = 1

while 1:
    state = GPIO.input(4)
    if (state == 0):
        print("Water Detected")
        state = 0
        
    else:
        state = 1

        
    if(prevState == 1 and state == 0):
        print("Start")
        camera.start_recording(date + '.h264')
        
    if(prevState == 0 and state == 1):
        camera.stop_recording()
        print("Stop")
        break

    prevState = state

print("Camera Done")
        
##camera.start_recording(filename)
##sleep(5)
##camera.stop_recording()
##completed_video = os.path(save_path, filename)

##camera.start_recording('my_video.h264')
##camera.wait_recording(60)
##camera.stop_recording()
