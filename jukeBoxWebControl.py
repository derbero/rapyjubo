#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
import RPi.GPIO as GPIO
import mpd

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

LED = 24
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

app = Flask(__name__)



##########################################
# some internal mpd functions
# end
##########################################
def mpdCloseConnection(client):
    """
    Closes the MPDClient connection.
    """
    #client.stop()
    #client.close()
    #client.disconnect()
    print()
    print("---------- BEGIN ---- mpdCloseConnection(client) ------------")
    print("killing mpd... ")
    client.kill()
    print("... mpd has been killed successfully!")
    print("---------- END   ---- mpdCloseConnection(client) ------------")

def mpdInitConnection():
    """
    Initializes a MPDClient connection.
    """
    print()
    print("---------- BEGIN ---- mpdCloseConnection(client) ------------")
    print("trying to connect to mpd...")
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
            #sleep(5)

    print("mpd connected")

    print(mpd_client.status()['state'])
    print("---------- END   ---- mpdCloseConnection(client) ------------")

def mpdNumberOfSongsInPlaylist(client):
    playlistLength = int(client.status()['playlistlength'])
    print ("playlistLength: " + str(playlistLength))
    return playlistLength

def mpdPlaylistHasPreviousSong(client):
    hasPrevSong = False
    if (mpdActualPlaylistSongNumber(client) > 1):
        hasPrevSong = True
    else:
        hasPrevSong = False
    return hasPrevSong

def mpdPlaylistHasNextSong(client):
    print("---------- BEGIN ---- mpdPlaylistHasNextSong(client) ------------")
    hasNextSong = False
    noOfSongsInList = mpdNumberOfSongsInPlaylist(client)
    actualSongNumber = mpdActualPlaylistSongNumber(client)
    print("noOfSongsInList: " + str(noOfSongsInList))
    print("actualSongNumber: " + str(actualSongNumber))
    print("( noOfSongsInList > actualSongNumber ): " + str(( noOfSongsInList > actualSongNumber )))
    if ( noOfSongsInList > actualSongNumber ):
        hasNextSong = True
    else:
        hasNextSong = False

    print("hasNextSong: " + str(hasNextSong))
    print("---------- END   ---- mpdPlaylistHasNextSong(client) ------------")
    return hasNextSong

def mpdActualPlaylistSongNumber(client):
    actualSongNumberInPlaylist = 1 + int(client.status()['song'])
    #print("actualSongNumberInPlaylist: " + str(actualSongNumberInPlaylist))
    return actualSongNumberInPlaylist
##########################################
# some internal mpd functions
# end
##########################################
##########################################
# callback functions for the buttons
# begin
##########################################
def mpdVolumeUp(channel):
    print("---------- BEGIN ---- mpdVolumeUp ------------")
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
    if mpdPlaylistHasNextSong(mpd_client) is True:
        mpd_client.next()
        print("player has gone to next song " + str(mpd_client.status()['song']))
    else:
        print("no next song in playlist. staying with actual song: " + str(mpd_client.status()['song']))

def mpdPrevious(channel):
    # previous title
    if mpdPlaylistHasPreviousSong(mpd_client) is True:
        mpd_client.previous()
        print ("player has gone to previous song " + str(mpd_client.status()['song']))
    else:
        print("no previous song in playlist. staying with actual song: " + str(mpd_client.status()['song']))
##########################################
# callback functions for the buttons
# end
##########################################


mpd_client = mpdInitConnection()

@app.route('/api/mpd/volumeup')
def mpd_volumeup():
    mpdVolumeUp(None)


@app.route('/api/led/on')
def led_on():
    GPIO.output(LED,GPIO.HIGH)
    return jsonify(led=GPIO.input(LED))

@app.route('/api/led/off')
def led_off():
    GPIO.output(LED,GPIO.LOW)
    return jsonify(led=GPIO.input(LED))

@app.route('/api/led/toggle')
def led_togggle():
    GPIO.output(LED,not GPIO.input(LED))
    return jsonify(led=GPIO.input(LED))

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")