from fastapi import APIRouter, HTTPException
from routers.library.library_responses import (
    ArtistListModel, AlbumListModel, AlbumModel)
from components.library import Library
from starlette.responses import FileResponse


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


@router.get("/library/cover_path/{artist}/{album}",
            tags=[tag],
            responses={404: {"description": "Cover not found."}},
            response_model=AlbumModel)
async def get_cover_path(artist: str, album: str):
    """
    Return a list of albums for the specified artist.
    """
    cover = library.get_cover_path(artist, album)
    if not cover:
        raise HTTPException(status_code=404, detail="Cover not found.")
    return {
        "artist":  artist,
        "album": album,
        "cover": cover}


@router.get("/library/cover/{artist}/{album}",
            tags=[tag],
            responses={404: {"description": "Cover not found."},
                       200: {"content": {"image/png": {}}}})
async def get_cover(artist: str, album: str):
    """
    Return a list of albums for the specified artist.
    """
    cover = library.get_cover_path(artist, album)
    if not cover:
        raise HTTPException(status_code=404, detail="Cover not found.")
    return FileResponse(cover, media_type="image/png")


@router.get("/library/random_album",
            tags=[tag],
            response_model=AlbumModel)
async def get_random_album():
    """
    Return a randomly selected album.
    """
    artist, album = library.get_random_album()
    cover = library.get_cover_path(artist, album)
    return {
        "artist":  artist,
        "album": album,
        "cover": cover}
