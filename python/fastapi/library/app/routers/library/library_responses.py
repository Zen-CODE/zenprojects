from pydantic import BaseModel
from typing import List


class ArtistListModel(BaseModel):
    """
    The list of artists in our music library.
    """
    artists: List[str] = []


class AlbumListModel(BaseModel):
    """
    The list of albums for a given artist
    """
    artist: str
    albums: List[str] = []


class CoverModel(BaseModel):
    """
    The full path to the cover art for the given artist and album.
    """
    artist: str
    album: str
    cover: str
