#!/usr/bin/env python
# -*- coding: utf-8 -*-

# which device is your RFID reader?
rfidreader = "/dev/input/event0"

# MPD PARAMETERS
print ("Setting mpd parameters...")
# Only if you know what you're doing! #
HOST = 'localhost' #
#HOST = '192.168.0.125' #
PORT = '6601' #
PASSWORD = False #
CON_ID = {'host':HOST, 'port':PORT} #
print ("... done!")


# GPIO PARAMETERS
print ("Setting gpio parameters...")
POWEROFF_TIME = 10
OUT_PIN_POWER = 7               # GPIO04: 07, GND: 06, POWER: 04 (5V)
IN_PIN_VOLUME_UP = 11           # GPIO17: 11, GND: 09
IN_PIN_VOLUME_DOWN = 13         # GPIO27: 13, GND: 14
IN_PIN_TRACK_NEXT = 18          # GPIO24: 18, GND: 20
IN_PIN_TRACK_PREVIOUS = 29      # GPIO05: 29, GND: 30
IN_PIN_TOGGLE_PLAY_PAUSE = 33   # GPIO13: 33, GND: 34
print ("...done!")
