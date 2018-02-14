#!/usr/bin/env python
import csv
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
outputFile = "/home/pi/Documents/Data/" + "Output.csv"

FLOW_SENSOR = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)
prevSoap = 1
soap = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)
prevWater = OFF
water = OFF

global waterOn
waterOn= False
soapOn = False
recordCount = 0
global timeCount
timeCount = 0
soapCount = 0
debounceTime = 0


    
def writeToCSV(soapNum, rotations):
    
    if os.path.exists(outputFile) is True:
        
        if startRecording is True:
            return;
        else:
            date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
            waterNum = 1
            with open(outputFile, 'a') as outcsv:
                 writer = csv.writer(outcsv)
                 writer.writerow([date, waterNum, soapNum, rotations/10])
            print("Wrote to file Output.csv")

    else:
        with open(outputFile, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(['Date-Time', 'Number of Water Events', 'Number of Soap Events', 'Rotations/sec'])

        print("Created new file Output.csv")

global flowCount
flowCount = 0

def countPulse(channel):
    global flowCount
    global waterOn
    global filename
    global timeCount
    global startRecording
    startRecording = False
    flowCount = flowCount + 1
    print(flowCount)
    
    if(flowCount <= 1):
        waterOn = True
        startRecording = True
        print("Water Sensor On")
        timeCount = time.time();
        writeToCSV(0, 0);
        startRecording = False
        print(datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S"))
        recordCount = 1
        filename = date + '.h264'
        savePath = "/home/pi/Documents/Data/" + datetime.datetime.now().strftime("%m_%d_%Y")
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        completeVideo = os.path.join(savePath, filename)
        camera.start_recording(completeVideo)
        print("Camera started")
        
    
GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback = countPulse)
    
while True:
    
    soap = GPIO.input(6)
    
    #Soap Sensor Logic
    if(prevSoap == OFF and soap == ON and time.time() > debounceTime + 1):
        soapOn = True
        soapCount = soapCount + 1
        debounceTime = time.time()

        
    if(prevSoap == ON and soap == OFF):
        soapOn = False
        
    prevSoap = soap
                      
    if((waterOn is True) and (time.time() > timeCount + 10)):
        print("Stopped camera recording")
        print("Total number of rotations:")
        print(flowCount)
        rotations=flowCount
        camera.stop_recording()
        
        print("Water Sensor Stopped")
        recordCount = 0
        prevSoap = OFF
        soap = OFF
        water = 0
        flowCount = 0
        waterOn = False
        prevWater = 0
        timeCount = 0
        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        writeToCSV(soapCount,rotations)
        print("Soap Count: ")
        print(soapCount)
        print("Time:")
        print(date)
        soapCount = 0
        

print("Camera Done")
print("Soap Count: ")
print(soapCount);
        
