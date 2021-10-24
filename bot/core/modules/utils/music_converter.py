from dotenv import load_dotenv
from youtubesearchpython import VideosSearch

load_dotenv()


def get_song_url(arg):
    # if argument is a single spotify track, get youtube equivalent and return
    url = VideosSearch(arg, limit=1)
    return url.result()["result"][0]["link"]
