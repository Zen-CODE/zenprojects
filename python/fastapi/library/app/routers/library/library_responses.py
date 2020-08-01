from pydantic import BaseModel
from typing import List


class ArtistListModel(BaseModel):
    """
    The list of artists in our music library.
    """
    artists: List[str] = []


class AlbumListModel(BaseModel):
    """
    The list of albums for a given artist.
    """
    artist: str
    albums: List[str] = []


class AlbumModel(BaseModel):
    """
    The details of an album, inlcuding the full path to the cover art.
    """
    artist: str
    album: str
    cover: str


