#!/usr/bin/python

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time
from time import sleep


# power button has a LED that is connected to GND and GPIO 23
# goal is to let it blink for some time when we are shutting down
ledPin = 23
ledState = False

# button debounce time in seconds
debounceSeconds = 0.01

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(ledPin, True)
sleep(1)
GPIO.output(ledPin, False)
sleep(1)
GPIO.output(ledPin, True)
sleep(1)
GPIO.output(ledPin, False)
sleep(1)
GPIO.output(ledPin, True)
sleep(1)
GPIO.output(ledPin, False)
sleep(1)