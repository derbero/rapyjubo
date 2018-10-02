import spotipy
spotify = spotipy.Spotify()
results = spotify.search(q='artist:' + 'Bad Religion', type='artist')
print results
