from __future__ import print_function, unicode_literals
import time
import spotify
import threading

import spotipy
sp = spotipy.Spotify()

VARIOUS_ARTISTS_URIS = [
    'spotify:artist:0LyfQWJT6nXafLPZqxe9Of',
]
 
logged_in_event = threading.Event()
def connection_state_listener(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in_event.set()
 
config = spotify.Config()
config.cache_location = None
session = spotify.Session(config)
session.on(
    spotify.SessionEvent.CONNECTION_STATE_UPDATED,
    connection_state_listener)
 
username = raw_input('Username: ')
password = raw_input('Password: ')
 
session.login(username, password)
while not logged_in_event.wait(0.1):
    session.process_events()
 
artistname = 'Avicii' #raw_input('Artist: ')
search = session.search('artist:"{0}"'.format(artistname))
artist = search.load().artists[0]

print('Gathering albums for artist "%s"' % artist.link)

tracks = []
albums_full = []
albums = []

num_requests = 1
start = time.time() 
results = sp.artist_albums(str(artist.link), 
                            album_type='album,single', 
                            country='GB', 
                            limit=50, 
                            offset=0)
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])
    num_requests += 1
middle = time.time()
ids = []
for album in albums:
    ids.append(album['id'])
    if len(ids) == 20:
        albums_full.extend(sp.albums(ids)['albums']) # API limits this to batches of 20
        num_requests += 1
        ids = []

if len(ids) > 0:
    albums_full.extend(sp.albums(ids)['albums'])
    num_requests += 1
    
for album in albums_full:
    tracks.extend(album['tracks']['items'])

end = time.time()

print('Found %d albums and %d tracks in %.3fs (%.3fs) using %d requests' % 
        (len(albums_full), len(tracks), end - start, end - middle, num_requests))
for album in sorted(albums_full, key=lambda a: a['name']):
    print("\t%s (%s) - %s (%s)" % (album['name'], 
                                   album['release_date'], 
                                   album['uri'], 
                                   ','.join([a['id'] for a in album['artists']]) ))

print("Found %d tracks" % len(tracks))

######

albums = []
albums_full = []
tracks = []

start = time.time() 
artistbrowse = artist.browse(type=spotify.ArtistBrowserType.NO_TRACKS)
artistbrowse.load()
for album in artistbrowse.albums:
    if album.is_available:
        #if album.artist.link.uri != artist.link.uri:
            #continue
        if album.type in [spotify.AlbumType.COMPILATION, spotify.AlbumType.UNKNOWN]:
            continue
        if album.artist.link.uri in VARIOUS_ARTISTS_URIS:
            continue
        albums.append(album.browse())

middle = time.time()
for album in albums:
    album.load()
    albums_full.append(album.album)
    tracks.extend(album.tracks)

end = time.time()        
print('Found %d albums and %d tracks in %.3fs (%.3fs)' % 
        (len(albums_full), len(tracks), end - start, end - middle))
for album in sorted(albums_full, key=lambda a: a.name):
    print("\t%s (%s) - %s (%s)" % (album.name, 
                                   album.year, 
                                   album.link, 
                                   album.artist.link.uri))
