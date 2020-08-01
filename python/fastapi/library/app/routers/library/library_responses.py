from pydantic import BaseModel
from typing import List


class ArtistListModel(BaseModel):
    """
    The a list of artists in out music library.
    """
    artists: List[str] = []


class AlbumListModel(BaseModel):
    """
    The return value of the listing for `get_artists`.
    """
    artist: str
    albums: List[str] = []
