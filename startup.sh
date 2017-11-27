# place in /etc/rc.local with filepath: .../healthyhands.py

sleep 10

/usr/bin/tvservice -o               # disable HDMI

echo none | sudo tee /sys/class/leds/led0/trigger # Set the Pi Zero ACT LED trigger to 'none'.

echo 1 | sudo tee /sys/class/leds/led0/brightness # Turn off the Pi Zero ACT LED.

iwconfig wlan0 txpower off          # turn off USB peripheral power

python /filepath/healthyhands.py&   # run program
