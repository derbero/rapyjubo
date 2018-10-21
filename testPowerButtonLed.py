#!/usr/bin/python

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time


# power button has a LED that is connected to GND and GPIO 23
# goal is to let it blink for some time when we are shutting down
ledPin = 23
ledState = False

# button debounce time in seconds
debounceSeconds = 0.01

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(LED, True)
sleep(1)
GPIO.output(LED, False)
sleep(1)
GPIO.output(LED, True)
sleep(1)
GPIO.output(LED, False)
sleep(1)
GPIO.output(LED, True)
sleep(1)
GPIO.output(LED, False)
sleep(1)