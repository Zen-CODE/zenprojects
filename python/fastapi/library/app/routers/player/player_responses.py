from pydantic import BaseModel
from typing import List


class StateModel(BaseModel):
    """
    The the state of the current player.
    """
    album: str = ""
    artist: str = ""
    cover: str = ""
    file_name: str = ""
    position: float = 0.0
    state: str = ""
    time_display: str = ""
    track: str = ""
    volume: float = 0.0


class MetaDataModel(BaseModel):
    """
    The the technical details of the currently playing track.
    """
    bitrate: int = 0
    channels: int = 0
    length: int = 0
    sample_rate: int = 0
