from fastapi import APIRouter, HTTPException
from routers.library.library_responses import ArtistListModel, AlbumListModel
from components.library import Library


router = APIRouter()
library = Library()
tag = "Library"


@router.get("/library/artists",
            tags=[tag],
            responses={404: {"description": "Library folder not found."}},
            response_model=ArtistListModel)
async def get_artists():
    """
    Return a list of artists in the music library.
    """
    artists = library.get_artists()
    if not artists:
        raise HTTPException(status_code=404, detail="Library folder not found")
    return {"artists": artists}


@router.get("/library/albums/{artist}",
            tags=[tag],
            responses={404: {"description": "Album folders not found."}},
            response_model=AlbumListModel)
async def get_albums(artist: str):
    """
    Return a list of albums for the specified artist.
    """
    albums = library.get_albums(artist)
    if not albums:
        raise HTTPException(status_code=404, detail="Album folders not found.")
    return {
        "artist":  artist,
        "albums": albums}
