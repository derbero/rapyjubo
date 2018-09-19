#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import types
import sys
from socket import error as SocketError
import mpd
#import mpc  # ?
from time import sleep, time
import RPi.GPIO as GPIO
import readchar

print ("Setting constants...")

global TEST_MPD_HOST, TEST_MPD_PORT, TEST_MPD_PASSWORD

TEST_MPD_HOST = "localhost"
TEST_MPD_PORT = "6600"
TEST_MPD_PASSWORD = ""
POWEROFF_TIME = 10

OUT_PIN_POWER = 3

IN_PIN_VOLUME_UP = 12
IN_PIN_VOLUME_DOWN = 13
IN_PIN_TRACK_NEXT = 15
IN_PIN_TRACK_PREVIOUS = 16
IN_PIN_TOGGLE_PLAY_PAUSE = 11

print ("...done!")


# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# To configure a channel as an input:
# GPIO.setup(channel, GPIO.IN)
# [IN_PIN_VOLUME_UP, IN_PIN_VOLUME_DOWN, IN_PIN_TRACK_NEXT, IN_PIN_TRACK_PREVIOUS, IN_PIN_TOGGLE_PLAY_PAUSE]
GPIO.setup(IN_PIN_VOLUME_UP, GPIO.IN)
GPIO.setup(IN_PIN_VOLUME_DOWN, GPIO.IN)
GPIO.setup(IN_PIN_TRACK_NEXT, GPIO.IN)
GPIO.setup(IN_PIN_TRACK_PREVIOUS, GPIO.IN)
GPIO.setup(IN_PIN_TOGGLE_PLAY_PAUSE, GPIO.IN)

# To set up a channel as an output:
# GPIO.setup(channel, GPIO.OUT)
# You can also specify an initial value for your output channel:
# GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
# Beim Starten des Programmes wird die LED vom Power Button auf AN geschaltet
GPIO.setup(OUT_PIN_POWER, GPIO.OUT, initial=GPIO.HIGH)


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


#print ("trying to get mpd_client = mpd.MPDClient()...")
#mpd_client = mpd.MPDClient()
#print("...done")


def close_mpd_connection(client):
    """
    Closes an MPDClient connection.
    """
    client.stop()
    #client.close()
    #client.disconnect()
    client.kill()

def init_mpd_connection():
    print("traying to connect to mpd...")
    mpd_client = mpd.MPDClient()
    #print(mpd_client.status()['state'])
    connected = False
    while connected == False:
        connected = True
        try:
            mpd_client.connect(TEST_MPD_HOST, TEST_MPD_PORT)
        #except SocketError as e:
        except mpd.ConnectionError as err:
            if "Already connected" in err:
                print("Error...")
                print (err)
                #return True, None
                return mpd_client
            else:
                return False, err
        #    connected = False
        if connected == True and TEST_MPD_PASSWORD != None:
            try:
                mpd_client.password(TEST_MPD_PASSWORD)
            except mpd.CommandError as e:
                connected = False
        if connected == False:
            print("Couldn't connect to mpd. Retrying")
            sleep(5)

    print("mpd connected")

    print(mpd_client.status()['state'])

def mpdNumberOfSongsInPlaylist(client):
    playlistLength = int(client.status['playlistlength'])
    return playlistLength

def mpdPlaylistHasPreviousSong(client):
    if (mpdActualPlaylistSongNumber(client) > 1):
        hasPrevSong = True
    else:
        hasPrevSong = False
    return hasPrevSong

def mpdPlaylistHasNextSong(client):
    if (mpdNumberOfSongsInPlaylist(client) > mpdActualPlaylistSongNumber(client)):
        hasNextSong = True
    else:
        hasNextSong = False
    return hasNextSong

def mpdActualPlaylistSongNumber(client):
    actualSongNumberInPlaylist = int(client.status['song'])


def mpdVolumeUp(channel):
    # set volume to +10
    if (int(mpd_client.status()['volume']) <= 90):
        mpd_client.setvol(int(mpd_client.status()['volume']) + 10)
        print ("player volume set up to " + str(mpd_client.status()['volume']))
    else:
        print("player already set to maximum volume: " + str(mpd_client.status()['volume']))

def mpdVolumeDown(channel):
    # set volume to -10
    if (int(mpd_client.status()['volume']) >= 10):
        mpd_client.setvol(int(mpd_client.status()['volume']) - 10)
        print("player volume set down to " + str(mpd_client.status()['volume']))
    else:
        print("player already set to minimum volume: " + str(mpd_client.status()['volume']))

def mpdPlayPauseToggle(channel):
    # toggle play pause
    mpd_client.pause()
    print("player in state " + str(mpd_client.status()['state']))

def mpdNext(channel):
    # next title
    if mpdPlaylistHasNextSong(mpd_client):
        mpd_client.next()
        print("player has gone to next song " + str(mpd_client.status()['song']))
    else:
        print("no next song in playlist. staying with actual song: " + str(mpd_client.status()['song']))

def mpdPrevious(channel):
    # previous title
    if mpdPlaylistHasPreviousSong(mpd_client):
        mpd_client.previous()
        print ("player has gone to previous song " + str(mpd_client.status()['song']))
    else:
        print("no previous song in playlist. staying with actual song: " + str(mpd_client.status()['song']))

def mpdLoadAndPlayPlaylist(playlistId):
    try:
        print("trying to load playlist..." + str(playlistId))
        mpd_client.load(str(playlistId))
        print("... playlist " + str(playlistId) + " loaded successfully")
    except:
        print("... error while loading playlist")

    try:
        print("trying to start playing ...")
        mpd_client.play(0)
        print("... playing")
    except:
        print("... error while trying to play")


GPIO.add_event_detect(IN_PIN_VOLUME_UP, GPIO.RISING, callback=mpdVolumeUp, bouncetime=200)  # add rising edge detection on a channel
GPIO.add_event_detect(IN_PIN_VOLUME_DOWN, GPIO.RISING, callback=mpdVolumeDown, bouncetime=200)
GPIO.add_event_detect(IN_PIN_TRACK_NEXT, GPIO.RISING, callback=mpdNext, bouncetime=200)
GPIO.add_event_detect(IN_PIN_TRACK_PREVIOUS, GPIO.RISING, callback=mpdPrevious, bouncetime=200)
GPIO.add_event_detect(IN_PIN_TOGGLE_PLAY_PAUSE, GPIO.RISING, callback=mpdPlayPauseToggle, bouncetime=200)



mpd_client = init_mpd_connection()
print("trying to clear...")
mpd_client.clear()
print("...done")

#print("trying to load playlist...")
#mpd_client.load("Benjamin Bluemchen_02 Rettet den Zoo")
#print("...done")

#print("trying to play...")
#mpd_client.play(0)
#print("...done")
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
        rfid_input = input('Enter your input:')
        mpdLoadAndPlayPlaylist(rfid_input)
#       # manual_control_input = str(input("enter command: "))
#       print ("enter command: ")
#       manual_control_input = readchar.readkey()
#       print('Input: ')
#       print(manual_control_input)
#         print(type(manual_control_input))
#
#         print ("trying to execute command...")
#         print("Volume status: " + str(mpd_client.status()['volume']))
#         print("Type: " + str(type(mpd_client.status()['volume'])))
#
#         if (manual_control_input == 's'):
#             # toggle play pause
#             mpd_client.pause()
#             print("player in state " + mpd_client.status()['state'])
#         elif (manual_control_input == 'w'):
#             # set volume to +10
#             if (int(mpd_client.status()['volume']) <= 90):
#                 mpd_client.setvol(int(mpd_client.status()['volume']) + 10)
#                 print ("player volume set up to " + mpd_client.status()['volume'])
#             else:
#                 print("player already set to maximum volume: " + mpd_client.status()['volume'])
#         elif (manual_control_input == 'x'):
#             # set volume to -10
#             if (int(mpd_client.status()['volume']) >= 10):
#                 mpd_client.setvol(int(mpd_client.status()['volume']) - 10)
#                 print("player volume set down to " + mpd_client.status()['volume'])
#             else:
#                 print("player already set to minimum volume: " + mpd_client.status()['volume'])
#         elif (manual_control_input == 'a'):
#             # previous title
#             mpd_client.previous()
#             print("player has gone to song " + mpd_client.status()['song'])
#         elif (manual_control_input == 'd'):
#             # previous title
#             mpd_client.next()
#             print ("player has gone to song " + mpd_client.status()['song'])
#         else:
#             close_mpd_connection(mpd_client)
#             break

#    except:
#    print("Exception raised.")
    except KeyboardInterrupt: #Strg-C wird gedrückt
        print("Exception raised.")
        print("GPIO.cleanup()...")
        GPIO.cleanup()
        print("GPIO.cleanup()... done")
        print("close_mpd_connection()...")
        close_mpd_connection(mpd_client)
        print("close_mpd_connection()... done")
