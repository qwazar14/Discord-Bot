import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import re
from youtubesearchpython import VideosSearch

load_dotenv()

auth_manager = SpotifyClientCredentials(client_id=os.environ.get('d508adcadbe04b1aab0d1967ea8fd692'),
                                        client_secret=os.environ.get('aed386d92858434188b9a684962ba996'))
sp_client = spotipy.Spotify(auth_manager=auth_manager)


def get_song_url(arg):
    # if argument is a single spotify track, get youtube equivalent and return
    if "spotify" in arg:
        track_id = re.search(r"/track/(\S{22})", arg).group(1)
        track = sp_client.track(track_id)['name'] + " - " + sp_client.track(track_id)['album']['artists'][0]['name']
        url = VideosSearch(track, limit=1)
        return url.result()["result"][0]["link"]
    else:
        # else if argument is a track name, get youtube url and return
        url = VideosSearch(arg, limit=1)
        return url.result()["result"][0]["link"]


def get_spotify_playlist(spotify_url):
    playlist_id = re.search(r"/playlist/(\S{22})", spotify_url).group(1)
    lst = []
    for track in sp_client.playlist_tracks(playlist_id)["items"]:
        song = track['track']['name']
        artist = track['track']['album']['artists'][0]['name']
        tmp = song + " - " + artist
        lst.append(tmp)

    return lst
