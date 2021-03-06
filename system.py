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


outputFile = "/home/pi/Documents/Data/" + "OutputData.csv"

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
global soapStartTime
global soapEndTime
soapStartTime = 0
soapEndTime = 0
timeCount = 0
soapCount = 0
debounceTime = 0
soapDebounceTime = 0
soapTimeArray = []

    
def writeToCSV(soapTimeArray, soapNum, rotations):
    
    if os.path.exists(outputFile) is True:
        
        if startRecording is True:
            return;
        else:
            waterNum = 1
            with open(outputFile, 'a') as outcsv:
                 writer = csv.writer(outcsv)
                 writer.writerow([date, round((rotations*1000/4380), 2), rotations/10, soapNum])
                 i = 0
                 while i < len(soapTimeArray) - 1:
                     writer.writerow(['', '', '', '', soapTimeArray[i], soapTimeArray[i+1]])
                     i = i + 2
            print("Wrote to file Output.csv")

    else:
        with open(outputFile, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(['Date-Time', 'Total Water Use (mL)', 'Rotations/sec', 'Number of Soap Events', 'Soap Start Time', 'Soap End Time'])

        print("Created new file Output.csv")

global flowCount
flowCount = 0

def countPulse(channel):
    global flowCount
    global waterOn
    global filename
    global timeCount
    global startRecording
    global date
    startRecording = False
    flowCount = flowCount + 1
    print(flowCount)
    timeCount = time.time()
    
    
    if(flowCount <= 1):
        waterOn = True
        startRecording = True
        print("Water Sensor On")
        timeCount = time.time();
        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S") 
        writeToCSV([0,0], 0, 0);
        startRecording = False

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
    
    if(vout > 26):
        soap = False
    else:
        soap = True
        #if (prevSoap == False):
            #print("Soap in Use")
    adc.stop_adc()
    
    #Soap Sensor Logic
    if(prevSoap == False and soap == True and (time.time() > soapDebounceTime + 0.5)):
        soapDebounceTime = time.time()
        soapStartTime = datetime.datetime.now().strftime("%H_%M_%S")
        soapOn = True
        soapCount = soapCount + 1
        soapTimeArray.append(soapStartTime)
        
    if(prevSoap == True and soap == False):
        soapEndTime = datetime.datetime.now().strftime("%H_%M_%S")
        soapOn = False
        soapTimeArray.append(soapEndTime)

        
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
        writeToCSV(soapTimeArray, soapCount,rotations)
        soapTimeArray = []
        print("Soap Count: ")
        print(soapCount)
        print("Time:")
        print(date)
        soapCount = 0
