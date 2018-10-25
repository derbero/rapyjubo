#!/usr/bin/python

# shutdown / power on Raspberry Pi with pushbutton

# pushbutton: NO connected to GPIO 3, normally open and shuts at button press
# Button press starts raspberry if off (connecting GPIO 3 to GND) and does nothing if raspberry is already on

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time
from time import sleep
import logging
import sys

# pushbutton: NC connected to GPIO 4 (former entry: 27), normally closed, and opens at button press
# we want a shutdown if button is pressed meaning  GPIO 4 (former entry: 27) opens
shutdownPin = 4

######### LOGGING #########
#logging.basicConfig(filename='listen4shutdown_running.log',level=logging.DEBUG)
def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('/home/pi/rapyjubo/listen4shutdown.log', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger
logger = setup_custom_logger('myapp')
#########################################


# power button has a LED that is connected to GND and GPIO 23
# goal is to let it blink for some time when we are shutting down
ledPin = 23
ledState = True

# button debounce time in seconds
deltaToShutdown = 1
# when second button is not pressed within 2 seconds, set back time of first button press
resetFirstButtonPressTime = 2

buttonPressedFirst = 0
buttonPressedSecond = 0
buttonPressedDelta = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(shutdownPin, GPIO.IN)
#GPIO.setup(shutdownPin, GPIO.IN)
#GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin, GPIO.OUT, initial=0)

buttonPressedTime = datetime.now()
elapsed = 0


def buttonStateChanged(pin):
 ledState = False
 #print("button pressed")
 global buttonPressedFirst
 global buttonPressedSecond
 global buttonPressedDelta

# if not (GPIO.input(pin)):
 if GPIO.input(shutdownPin) == 1:
         if (buttonPressedFirst == 0) or (time.time() - buttonPressedFirst > resetFirstButtonPressTime):
             print("FIRST button press")
             buttonPressedFirst = time.time()
             logger.info("FIRST button press: " + str(buttonPressedFirst))
         else:
            print("SECOND button press")
            buttonPressedSecond = time.time()
            logger.info("SECOND button press: " + str(buttonPressedSecond))
            buttonPressedDelta = buttonPressedSecond - buttonPressedFirst
            buttonPressedFirst = 0
            if buttonPressedDelta <= deltaToShutdown:
                print("BOTH button presses happenend within one second; delta: " + str(buttonPressedDelta))
                logger.info("BOTH button presses happenend within one second; delta: " + str(buttonPressedDelta))
                # toggle / blink ledPin for a while
                for i in range(1, 11):
                    ledState = not ledState
                    GPIO.output(ledPin, ledState)
                    sleep(0.1)
                # shutdown
                call(['shutdown', '-h', 'now'], shell=False)
 else:
         print("BUTTON released - not HANDLING THAT")

# subscribe to button presses
#GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged, bouncetime=200)
#GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged, bouncetime=200)
GPIO.add_event_detect(shutdownPin, GPIO.FALLING, callback=buttonStateChanged, bouncetime=200)
#GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged)

try:
    while True:
         # sleep to reduce unnecessary CPU usage
         time.sleep(5)
except KeyboardInterrupt:
  GPIO.cleanup()
  print("\nBye!")
  logger.info("----- CLEAN EXIT -----")
