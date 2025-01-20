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

