#!/usr/bin/env python
import csv
import datetime
import time
import os
import RPi.GPIO as GPIO
import picamera
import time
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16 bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1
resistor = 1000
vin = 3.3
raw = 0
vout = 0
refresistor1 = 10
refresistor2 = 0
buffer = 0


camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
outputFile = "/home/pi/Documents/Data/" + "Output.csv"

FLOW_SENSOR = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)
global prevSoap
prevSoap = False
global soap
soap = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)
prevWater = False
water = False

global waterOn
waterOn= False
soapOn = False
recordCount = 0
global timeCount
timeCount = 0
soapCount = 0
debounceTime = 0
soapDebounceTime = 0


    
def writeToCSV(soapNum, rotations):
    
    if os.path.exists(outputFile) is True:
        
        if startRecording is True:
            return;
        else:
            date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
            waterNum = 1
            with open(outputFile, 'a') as outcsv:
                 writer = csv.writer(outcsv)
                 writer.writerow([date, waterNum, soapNum, rotations/10, rotations*1000/4380])
            print("Wrote to file Output.csv")

    else:
        with open(outputFile, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(['Date-Time', 'Number of Water Events', 'Number of Soap Events', 'Rotations/sec', 'Total Water Use (mL)'])

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
    timeCount = time.time()
    
    
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
    
    adc.start_adc(0, gain= GAIN)
    value = adc.get_last_result()
    vout = (vin / resistor)*value
    buffer = (vin/vout) -1
    refesistor2 = refresistor1 / buffer
    
    if(vout > 44):
        soap = False
    else:
        soap = True
        #if (prevSoap == False):
            #print("Soap in Use")
    adc.stop_adc()
    
    #Soap Sensor Logic
    if(prevSoap == False and soap == True and (time.time() > soapDebounceTime + 0.5)):
        soapDebounceTime = time.time()
        soapOn = True
        soapCount = soapCount + 1
        
    if(prevSoap == True and soap == False):
        soapOn = False
        
    prevSoap = soap
                      
    if((waterOn is True) and (time.time() > timeCount + 5)):
        print("Stopped camera recording")
        print("Total number of rotations:")
        print(flowCount)
        rotations=flowCount
        camera.stop_recording()
        
        print("Water Sensor Stopped")
        recordCount = 0
        prevSoap = False
        soap = False
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
        
        


