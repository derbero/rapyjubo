#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import types
import sys
from socket import error as SocketError
from mpd import (MPDClient, CommandError)
import mpd
import threading
#import mpc  # ?
from time import sleep, time


#########  MPD PARAMETERS  ##############
# Only if you know what you're doing! #
HOST = 'localhost' #
#HOST = '192.168.0.125' #
PORT = '6600' #
PASSWORD = False #
CON_ID = {'host':HOST, 'port':PORT} #
#########################################




##########################################
# some internal mpd functions
# end
##########################################


def mpdConnect(client, con_id):
   """
   Simple wrapper to connect MPD.
   """
   print()
   print("---------- BEGIN ---- mpdConnect(client, con_id) ------------")
   print("trying to connect to mpd...")
   try:
       client.connect(**con_id)
   except SocketError as err:
       print("... mpd connection FAILED: " + err)
       return False
   print("... mpd connection SUCCESSFULL")
   print("mpd_client.status()['state']: " + mpd_client.status()['state'])
   print("---------- END   ---- mpdConnect(client, con_id) ------------")
   return True


def mpdCloseConnection(client):
    """
    Closes the MPDClient connection.
    """
    print()
    print("---------- BEGIN ---- mpdCloseConnection(client) ------------")
    print("trying to stop mpd...")
    client.stop()
    print("... stopped")
    print("trying to close mpd...")
    client.close()
    print("... closed")
    print("trying to disconnect...")
    client.disconnect()
    print("... disconnected")
    #print("killing mpd... ")
    #client.kill()
    #print("... mpd has been killed successfully!")
    print("---------- END   ---- mpdCloseConnection(client) ------------")

# def mpdInitConnection():
#     """
#     Initializes a MPDClient connection.
#     """
#     global mpd_client
#     print()
#     print("---------- BEGIN ---- mpdInitConnection(client) ------------")
#     print("trying to connect to mpd...")
#     mpd_client = mpd.MPDClient()
#     #print(mpd_client.status()['state'])
#     connected = False
#     while connected == False:
#         connected = True
#         try:
#             mpd_client.connect(TEST_MPD_HOST, TEST_MPD_PORT)
#         #except SocketError as e:
#         except mpd.ConnectionError as err:
#             if "Already connected" in err:
#                 print("Error...")
#                 print (err)
#                 #return True, None
#                 return mpd_client
#             else:
#                 return False, err
#         #    connected = False
#         if connected == True and TEST_MPD_PASSWORD != None:
#             try:
#                 mpd_client.password(TEST_MPD_PASSWORD)
#             except mpd.CommandError as e:
#                 connected = False
#         if connected == False:
#             print("Couldn't connect to mpd. Retrying")
#             sleep(0.5)
#
#     print("mpd connected")
#
#     print("mpd_client.status()['state']" + mpd_client.status()['state'])
#     print("---------- END   ---- mpdInitConnection(client) ------------")

def mpdNumberOfSongsInPlaylist(client):
    #print()
    #print("---------- BEGIN ---- mpdNumberOfSongsInPlaylist(client) ------------")
    playlistLength = int(client.status()['playlistlength'])
    #print ("playlistLength: " + str(playlistLength))
    #print("---------- END   ---- mpdNumberOfSongsInPlaylist(client) ------------")
    return playlistLength

def mpdPlaylistHasPreviousSong(client):
    print()
    print("---------- BEGIN ---- mpdPlaylistHasNextSong(client) ------------")
    actualSongNumber = mpdActualPlaylistSongNumber(client)
    print("actualSongNumber: " + str(actualSongNumber))
    print("(mpdActualPlaylistSongNumber(client) > 1): " + str(mpdActualPlaylistSongNumber(client) > 1))
    if (mpdActualPlaylistSongNumber(client) > 1):
        hasPrevSong = True
    else:
        hasPrevSong = False
    print("hasPrevSong: " + str(hasPrevSong))
    return hasPrevSong

def mpdPlaylistHasNextSong(client):
    print()
    print("---------- BEGIN ---- mpdPlaylistHasNextSong(client) ------------")
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
    #print
    #print("---------- BEGIN ---- mpdActualPlaylistSongNumber(client) ------------")
    actualSongNumberInPlaylist = 1 + int(client.status()['song'])
    #print("actualSongNumberInPlaylist : " + str(actualSongNumberInPlaylist ))
    #print("---------- END   ---- mpdActualPlaylistSongNumber(client) ------------")
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
    print()
    print("---------- BEGIN ---- mpdVolumeUp ------------")
    # set volume to +10
    if (int(mpd_client.status()['volume']) <= 90):
        mpd_client.setvol(int(mpd_client.status()['volume']) + 10)
        print ("player volume set up to " + str(mpd_client.status()['volume']))
    else:
        if(int(mpd_client.status()['volume']) < 100):
            mpd_client.setvol(100)
            print ("player volume set up to " + str(mpd_client.status()['volume']))
        else:
            print("player already set to maximum volume: " + str(mpd_client.status()['volume']))

def mpdVolumeDown(channel):
    # set volume to -10
    print()
    if (int(mpd_client.status()['volume']) >= 10):
        mpd_client.setvol(int(mpd_client.status()['volume']) - 10)
        print("player volume set down to " + str(mpd_client.status()['volume']))
    else:
        if (int(mpd_client.status()['volume']) > 0):
            mpd_client.setvol(0)
            print ("player volume set up to " + str(mpd_client.status()['volume']))
        else:
            print("player already set to minimum volume: " + str(mpd_client.status()['volume']))

def mpdPlayPauseToggle(channel):
    # toggle play pause
    print()
    mpd_client.pause()
    print("player in state " + str(mpd_client.status()['state']))

def mpdNext(channel):
    # next title
    print()
    if mpdPlaylistHasNextSong(mpd_client) is True:
        mpd_client.next()
        print("player has gone to next song " + str(mpd_client.status()['song']))
    else:
        print("no next song in playlist. staying with actual song: " + str(mpd_client.status()['song']))

def mpdPrevious(channel):
    # previous title
    print()
    if mpdPlaylistHasPreviousSong(mpd_client) is True:
        mpd_client.previous()
        print ("player has gone to previous song " + str(mpd_client.status()['song']))
    else:
        print("no previous song in playlist. staying with actual song: " + str(mpd_client.status()['song']))
##########################################
# callback functions for the buttons
# end
##########################################

def mpdLoadAndPlayPlaylist(playlistId):
    #global mpd_client
    try:
        print()
        print("trying to clear playlist ...")
        mpd_client.clear()
        print("... playlist cleared")
        try:
            print()
            print("trying to load playlist..." + str(playlistId))
            mpd_client.load(str(playlistId))
            print("... playlist " + str(playlistId) + " loaded successfully")
            try:
                print()
                print("trying to start playing ...")
                mpd_client.play(0)
                print("... playing")
                return True
            except:
                print("... error while trying to play")
                return False
        except:
            print("... error while loading playlist")
            return False
    except:
        print("... error while clearing playlist")
        return False
