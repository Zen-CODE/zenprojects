"""This file contains classes for interaction with the Zenplayer instance."""
from dataclasses import dataclass, asdict

ZENPLAYER_UWL = "http://127.0.0.1:9001/"


@dataclass
class NowPlaying:
    artist: str
    album: str
    track: int


class ZenFetcher:
    """This class retrieve info from the ZePlayer instance."""

    @staticmethod
    def now_playing():
        """Return the 'Now playing' data."""
        return asdict(NowPlaying("artist", "album", 1))
