#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import types
import sys
from socket import error as SocketError
from mpd import (MPDClient, CommandError)
import mpd
import threading
from time import sleep, time
import RPi.GPIO as GPIO
import readchar
import logging
#import getopt
#import shelve
#import ConfigParser
from conf import *
from evdev import InputDevice, categorize, ecodes

from fin_mpdwrapper import *
from fin_config import *


######### LOGGING #########
logging.basicConfig(filename='jukeboxLog.log',level=logging.DEBUG)
#########################################

######### USING_MANUAL_INPUT #########
USING_MANUAL_INPUT = False
#########################################










# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)


# To configure a channel as an input:
# GPIO.setup(channel, GPIO.IN)
# [IN_PIN_VOLUME_UP, IN_PIN_VOLUME_DOWN, IN_PIN_TRACK_NEXT, IN_PIN_TRACK_PREVIOUS, IN_PIN_TOGGLE_PLAY_PAUSE]
#GPIO.setup(IN_PIN_VOLUME_UP, GPIO.IN)
#GPIO.setup(IN_PIN_VOLUME_DOWN, GPIO.IN)
#GPIO.setup(IN_PIN_TRACK_NEXT, GPIO.IN)
#GPIO.setup(IN_PIN_TRACK_PREVIOUS, GPIO.IN)
#GPIO.setup(IN_PIN_TOGGLE_PLAY_PAUSE, GPIO.IN)

GPIO.setup(IN_PIN_VOLUME_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN_PIN_VOLUME_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN_PIN_TRACK_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN_PIN_TRACK_PREVIOUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN_PIN_TOGGLE_PLAY_PAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# To set up a channel as an output:
# GPIO.setup(channel, GPIO.OUT)
# You can also specify an initial value for your output channel:
# GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
# Beim Starten des Programmes wird die LED vom Power Button auf AN geschaltet
GPIO.setup(OUT_PIN_POWER, GPIO.OUT, initial=GPIO.LOW)


# You can set up more than one channel per call (release 0.5.8 onwards). For example:
# chan_list = [11,12]    # add as many channels as you want!
# you can tuples instead i.e.:
#   chan_list = (11,12)
# GPIO.setup(chan_list, GPIO.OUT)

# Input
# To read the value of a GPIO pin:
# GPIO.input(channel)
# (where channel is the channel number based on the numbering system you have specified (BOARD or BCM)). This will return either 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.

# Output
# To set the output state of a GPIO pin:
# GPIO.output(channel, state)
# (where channel is the channel number based on the numbering system you have specified (BOARD or BCM)).
# State can be 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.
# Output to several channels
# You can output to many channels in the same call (release 0.5.8 onwards). For example:
# chan_list = [11,12]                             # also works with tuples
# GPIO.output(chan_list, GPIO.LOW)                # sets all to GPIO.LOW
# GPIO.output(chan_list, (GPIO.HIGH, GPIO.LOW))   # sets first HIGH and second LOW

# To clean up at the end of your script:
# GPIO.cleanup()


print ("trying to get mpd_client = mpd.MPDClient()...")
mpd_client = mpd.MPDClient()
print("...done")




def swipe():
	# this is the rfid reader
	dev = InputDevice(rfidreader)
	# grab the rfid reader device
	dev.grab()
	cardnumber = []
	# wait for events from the rfid reader
	for event in dev.read_loop():
		# if we get a "key pressed down" event
		if event.type == ecodes.EV_KEY and event.value == 1:
			# if it is the enter key we've hit the end of a card number
			if event.code == 28:
				# merge the list in to a string
				card = ''.join(str(num) for num in cardnumber)
				# return the card number
				return card
			else:
				# the event code is 1 more than the actual number key
				number = event.code - 1
				# except for event id 10, which is actually KP_0
				if number == 10:
					number = 0
				# stick the number onto the end of our list
				cardnumber.append(number)









##########################################
# some internal gpio functions
# begin
##########################################
def gpioCleanup():
    """
    just cleans the GPIO
    """
    print()
    print("---------- BEGIN ---- gpioCleanup() ------------")
    print("cleaning up...")
    GPIO.cleanup()
    print("... clean")
    print("---------- END   ---- gpioCleanup() ------------")
##########################################
# some internal gpio functions
# end
##########################################



GPIO.add_event_detect(IN_PIN_VOLUME_UP, GPIO.RISING, callback=mpdVolumeUp, bouncetime=200)  # add rising edge detection on a channel
GPIO.add_event_detect(IN_PIN_VOLUME_DOWN, GPIO.RISING, callback=mpdVolumeDown, bouncetime=200)
GPIO.add_event_detect(IN_PIN_TRACK_NEXT, GPIO.RISING, callback=mpdNext, bouncetime=200)
GPIO.add_event_detect(IN_PIN_TRACK_PREVIOUS, GPIO.RISING, callback=mpdPrevious, bouncetime=200)
GPIO.add_event_detect(IN_PIN_TOGGLE_PLAY_PAUSE, GPIO.RISING, callback=mpdPlayPauseToggle, bouncetime=200)

#GPIO.add_event_detect(OUT_PIN_POWER, GPIO.LOW, callback=shutMeDown, bouncetime=200)


#mpd_client = mpdInitConnection()
#if not mpdConnect(mpd_client, CON_ID):
#    exit(1)
mpdConnected = mpdConnect(mpd_client, CON_ID)
while (not mpdConnected):
	sleep(1)
    	mpdConnected = mpdConnect(mpd_client, CON_ID)

#print("trying to clear...")
#mpd_client.clear()
#print("...done")

#print("trying to load playlist...")
#mpd_client.load("Benjamin Bluemchen_02 Rettet den Zoo")
#print("...done")

#print("trying to play...")
#mpd_client.play(0)
#print("...done")

loadNewPlaylist = True


# MPD Ping Thread
mpdping_t = threading.Thread(target=mpd_ping, args = ()) # Create thread for pinging MPD
mpdping_t.daemon = True # Yep, it's a daemon, when main thread finish, this one will finish too
mpdping_t.start() # Start it!


while (True):
    try:
        sleep(1)
#        if GPIO.event_detected(IN_PIN_TOGGLE_PLAY_PAUSE):
#            mpd_client.PlayPauseToggle();
#            print('IN_PIN_TOGGLE_PLAY_PAUSE button pressed')
#        if GPIO.event_detected(IN_PIN_VOLUME_UP):
#            mpd_client.VolumeUp();
#            print('IN_PIN_VOLUME_UP button pressed')
        # ...
        if loadNewPlaylist == True:
            playlistLoadedSuccessfully = False
            while(not playlistLoadedSuccessfully):
                try:
                    print("Waiting for RFID card input:")
                    rfid_input = str(swipe()) # python2: raw_input; python3: input
                    #rfid_input = str(raw_input('Enter your playlist:'))
                    #python2: raw_input; python3: input
    	            print("Card read: " + rfid_input)
                except EOFError:
                    continue
                    # hier sollte noch ein logging hin, damit die IDs der Karten irgendwo sichtbar werden
                #logging.debug('This message should go to the log file')
                logging.info('RFID card read with ID: ' + str(rfid_input))
                #logging.warning('And this, too')
                if(rfid_input == 'x'):
                    break
                playlistLoadedSuccessfully = mpdLoadAndPlayPlaylist(rfid_input)
                loadNewPlaylist = False
        if USING_MANUAL_INPUT:
    #        manual_control_input = str(input("enter command: "))
            print ("enter command: ")
            manual_control_input = readchar.readkey()
            print("command entered: " + str(manual_control_input) + "; type of input: " + str(type(manual_control_input)))

            print ("trying to execute command...")
            print("Volume status: " + str(mpd_client.status()['volume']))
            #print("Type: " + str(type(mpd_client.status()['volume'])))

            if (manual_control_input == 's'):
                # toggle play pause
                #mpd_client.pause()
                #print("player in state " + mpd_client.status()['state'])
                mpdPlayPauseToggle(None)
            elif (manual_control_input == 'w'):
                # set volume to +10
                #if (int(mpd_client.status()['volume']) <= 90):
                #    mpd_client.setvol(int(mpd_client.status()['volume']) + 10)
                #    print ("player volume set up to " + mpd_client.status()['volume'])
                #else:
                #    print("player already set to maximum volume: " + mpd_client.status()['volume'])
                mpdVolumeUp(None)
            elif (manual_control_input == 'x'):
                # set volume to -10
                #if (int(mpd_client.status()['volume']) >= 10):
                #    mpd_client.setvol(int(mpd_client.status()['volume']) - 10)
                #    print("player volume set down to " + mpd_client.status()['volume'])
                #else:
                #    print("player already set to minimum volume: " + mpd_client.status()['volume'])
                mpdVolumeDown(None)
            elif (manual_control_input == 'a'):
                # previous title
                #mpd_client.previous()
                #print("player has gone to song " + mpd_client.status()['songid'])
                mpdPrevious(None)
            elif (manual_control_input == 'd'):
                # previous title
                #mpd_client.next()
                #print ("player has gone to song " + mpd_client.status()['songid'])
                mpdNext(None)
            elif (manual_control_input == 'l'):
                # go to beginning of while to be able to load new playlist
                loadNewPlaylist = True
                continue
            else:
                print("GPIO.cleanup()...")
                GPIO.cleanup()
                print("GPIO.cleanup()... done")
                mpdCloseConnection(mpd_client)
                break
        print ("mpd status " + str(mpd_client.status()))
#    except:
#    print("Exception raised.")
    except KeyboardInterrupt: #Strg-C wird gedrückt
        print("Exception raised.")
        print()
        print("GPIO.cleanup()...")
        GPIO.cleanup()
        print("GPIO.cleanup()... done")
        print()
        print("close_mpd_connection()...")
        mpdCloseConnection(mpd_client)
        print("close_mpd_connection()... done")
