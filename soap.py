#!/usr/bin/env python
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
adc.start_adc(0, gain= GAIN)

start = time.time()
while (time.time() - start) <= 25.0:

    value = adc.get_last_result()
    vout = (vin / resistor)*value
    buffer = (vin/vout) -1
    refesistor2 = refresistor1 / buffer
    print('Voltage:{0}'.format(vout))
    print('Resistance:{0}'.format(refresistor2))
    print('Channel 0:{0}'.format(value))
    time.sleep(0.5)
    
adc.stop_adc()
