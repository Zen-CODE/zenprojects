from pydantic import BaseModel
from typing import List


class ArtistListModel(BaseModel):
    """
    The return value of the listing for `get_artists`.
    """
    artists: List[str] = []
