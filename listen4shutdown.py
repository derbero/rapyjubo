#!/usr/bin/python

# shutdown / power on Raspberry Pi with pushbutton

# pushbutton: NO connected to GPIO 3, normally open and shuts at button press
# Button press starts raspberry if off (connecting GPIO 3 to GND) and does nothing if raspberry is already on 

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time

# pushbutton: NC connected to GPIO 27, normally closed and opens at button press
# we want a shutdown if button is pressed meaning  GPIO 27 opens
shutdownPin = 27

# button debounce time in seconds
debounceSeconds = 0.01

GPIO.setmode(GPIO.BCM)
GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(shutdownPin, GPIO.IN)
#GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

buttonPressedTime = datetime.now()

def buttonStateChanged(pin):
 print("button pressed")
 global buttonPressedTime

 if not (GPIO.input(pin)):
 # button is down
 print("not GPIO.input(pin)")
 # if buttonPressedTime is None:
         buttonPressedTime = datetime.now()
 else:
 print("GPIO.input(pin):")
 print(pin)
 # button is up
 #if buttonPressedTime is not None:
 elapsed = (datetime.now() - buttonPressedTime).total_seconds()
 buttonPressedTime = datetime.now()
 if elapsed >= debounceSeconds:
 # button pressed for a shorter time, also shutdown
 call(['shutdown', '-h', 'now'], shell=False)


# subscribe to button presses
GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged)

while True:
 # sleep to reduce unnecessary CPU usage
     time.sleep(5)

GPIO.cleanup()
