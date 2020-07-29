from pydantic import BaseModel
from typing import List


class ArtisListModel(BaseModel):
    """
    The return value listing for `get_artists`.
    """
    artists: List[str] = []
