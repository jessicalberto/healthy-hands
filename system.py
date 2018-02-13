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

def checkPath():
    currentDatePath = "/home/pi/Documents/Data/" + "OutputData.csv"
    if(os.path.exists(currentDatePath) is True):
        return True
    else:
        os.mkdir(currentDatePath)
        return False
    
def writeToCSV(soapNum):
    if os.path.exists(outputFile) is True:
        
        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        waterNum = 1
        with open(outputFile, 'w') as outcsv:
             writer = csv.writer(outcsv)
             writer.writerow([date, waterNum, soapNum])
        print("Wrote to file")

    else:
        with open(outputFile, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(['Date-Time'.encode(), 'Number of Water Events'.encode(), 'Number of Soap Events'.encode()])

        print("Created file")

global flowCount
flowCount = 0

def countPulse(channel):
    global flowCount
    global waterOn
    global filename
    global timeCount
    flowCount = flowCount + 1
    print(flowCount)
    
    if(flowCount <= 1):
        checkPath()
        waterOn = True
        print("Water Sensor On")
        timeCount = time.time();
        print(timeCount);
        recordCount = 1
        camera.start_recording(date + '.h264')
        print("Camera started")
        filename = date + '.h264'
    
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
        print(flowCount)
        camera.stop_recording()
        savePath = "/home/pi/Documents/Data/" + datetime.datetime.now().strftime("%m_%d_%Y")
        completeVideo = os.path.join(savePath, filename)
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
        writeToCSV(soapCount)
        print("Soap Count: ")
        print(soapCount);
        print(time.time());
        soapCount = 0
        

print("Camera Done")
print("Soap Count: ")
print(soapCount);
        

