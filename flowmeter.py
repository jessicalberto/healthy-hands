import RPi.GPIO as GPIO
import time, sys

FLOW_SENSOR = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

isFlowing = False

def countPulse(channel):
    isFlowing = True
    if(isFlowing == True):
        print('Water Flowing')

    
if GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse):
    print('Water Flowing')

else:
    print('Water Stopped')
    
while True:
    try:
        time.sleep(1)
    except Keyboardinterrupt:
        GPIO.cleanup()
        sys.exit()
