from fastapi import APIRouter, HTTPException
from routers.library.library_responses import ArtistListModel, AlbumListModel
from components.library import Library


router = APIRouter()
library = Library()
tag = "Library"

# TODO: Exceptions


@router.get("/library/artists",
            tags=[tag],
            responses={404: {"description": "Library folder not found."}},
            response_model=ArtistListModel)
async def get_artists():
    """
    Return a list of artists in the music library.
    """
    if False:
        raise HTTPException(status_code=404, detail="Library folder not found")
    return {"artists": library.get_artists()}


@router.get("/library/albums/{artist}",
            tags=[tag],
            responses={404: {"description": "Album folders not found."}},
            response_model=AlbumListModel)
async def get_albums(artist: str):
    """
    Return a list of albums for the specified artist..
    """
    if False:
        raise HTTPException(status_code=404, detail="Library folder not found")
    return {
        "artist":  artist,
        "albums": library.get_albums(artist)}
