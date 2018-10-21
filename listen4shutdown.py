#!/usr/bin/python

# shutdown / power on Raspberry Pi with pushbutton

# pushbutton: NO connected to GPIO 3, normally open and shuts at button press
# Button press starts raspberry if off (connecting GPIO 3 to GND) and does nothing if raspberry is already on 

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time
from time import sleep

# pushbutton: NC connected to GPIO 4 (former entry: 27), normally closed, and opens at button press
# we want a shutdown if button is pressed meaning  GPIO 4 (former entry: 27) opens
shutdownPin = 04

# power button has a LED that is connected to GND and GPIO 23
# goal is to let it blink for some time when we are shutting down
ledPin = 23
ledState = False

# button debounce time in seconds
debounceSeconds = 0.01

GPIO.setmode(GPIO.BCM)
GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(shutdownPin, GPIO.IN)
#GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin, GPIO.OUT, initial = 0)

buttonPressedTime = datetime.now()
elapsed = 0

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
         # toggle / blink ledPin for a while
         for i in range(1, 6):
             ledState = not ledState
             GPIO.output(ledPin, ledState)
             sleep(1)
         # shutdown  
         call(['shutdown', '-h', 'now'], shell=False)


# subscribe to button presses
GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged)

while True:
         # sleep to reduce unnecessary CPU usage
         time.sleep(5)

GPIO.cleanup()
