from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List


router = APIRouter()


class ArtisListModel(BaseModel):
    """
    The return value listing for `get_artists`.
    """
    artists: List[str] = []


@router.get("/library/get_artists",
            tags=["library"],
            responses={404: {"description": "Library folder not found."}},
            response_model=ArtisListModel)
async def get_artists():
    """
    Return a list of artist in the music library.
    """
    if False:
        raise HTTPException(status_code=404, detail="Library folder not found")
    return {"artists": ["artist1", "artists2"]}
