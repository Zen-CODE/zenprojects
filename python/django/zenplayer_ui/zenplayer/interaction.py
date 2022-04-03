"""This file contains classes for interaction with the Zenplayer instance."""
from dataclasses import dataclass, asdict
from requests import get
from json import loads

ZENPLAYER_URL = "http://127.0.0.1:9001/"


@dataclass
class NowPlaying:
    artist: str
    album: str
    track_number: int


class ZenFetcher:
    """This class retrieve info from the ZePlayer instance."""

    @staticmethod
    def now_playing():
        """Return the 'Now playing' data."""
        response = get(ZENPLAYER_URL + 'zenplaylist/get_current_info')
        data = loads(response.content)
        np = NowPlaying(
            artist=data['artist'],
            album=data['album'],
            track_number=data['track_number'])
        return asdict(np)
