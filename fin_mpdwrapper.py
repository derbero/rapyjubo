#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep, time



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
       print("... mpd connection FAILED: " + str(err))
       return False
   print("... mpd connection SUCCESSFULL")
   print("mpd_client.status()['state']: " + client.status()['state'])
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
#   print()
#   print("---------- BEGIN ---- mpdNumberOfSongsInPlaylist(client) ------------")
    playlistLength = int(client.status()['playlistlength'])
#   print ("playlistLength: " + str(playlistLength))
#   print("---------- END   ---- mpdNumberOfSongsInPlaylist(client) ------------")
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





def mpdLoadAndPlayPlaylist(client, playlistId):
    #global mpd_client
    try:
        print()
        print("trying to clear playlist ...")
        client.clear()
        print("... playlist cleared")
        try:
            print()
            print("trying to load playlist..." + str(playlistId))
            client.load(str(playlistId))
            print("... playlist " + str(playlistId) + " loaded successfully")
            try:
                print()
                print("trying to start playing ...")
                client.play(0)
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
