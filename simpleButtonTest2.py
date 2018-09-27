#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import types
import sys
from socket import error as SocketError
from mpd import (MPDClient, CommandError)
import mpd
import threading
# import mpc  # ?
from time import sleep, time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

IN_PIN_TOGGLE_PLAY_PAUSE = 11

# To configure a channel as an input:
# GPIO.setup(channel, GPIO.IN)
# [IN_PIN_VOLUME_UP, IN_PIN_VOLUME_DOWN, IN_PIN_TRACK_NEXT, IN_PIN_TRACK_PREVIOUS, IN_PIN_TOGGLE_PLAY_PAUSE]

#GPIO.setup(IN_PIN_TOGGLE_PLAY_PAUSE, GPIO.IN)
GPIO.setup(IN_PIN_TOGGLE_PLAY_PAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def mpdPlayPauseToggle(channel):
    # toggle play pause
    print("Button pressed!")
    #mpd_client.pause()
    #print("player in state " + str(mpd_client.status()['state']))



GPIO.add_event_detect(IN_PIN_TOGGLE_PLAY_PAUSE, GPIO.RISING, callback=mpdPlayPauseToggle, bouncetime=400)


while (True):
    try:
        sleep(1)
    except KeyboardInterrupt: #Strg-C wird gedrückt
        print("Exception raised.")
        print()
        print("GPIO.cleanup()...")
        GPIO.cleanup()
        print("GPIO.cleanup()... done")