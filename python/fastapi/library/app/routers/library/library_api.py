from fastapi import APIRouter, HTTPException
from app.routers.library.library_responses import (
    ArtistListModel, AlbumListModel, AlbumModel, PathModel, TrackListModel,
    SearchModel)
from app.components.library import Library
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


@router.get("/library/cover/{artist}/{album}",
            tags=[tag],
            responses={404: {"description": "Cover not found."},
                       200: {"content": {"image/png": {}}}})
async def get_cover(artist: str, album: str):
    """
    Returns image data given a valid artist and album, otherwise
    returns a 404.
    """
    cover = library.get_cover_path(artist, album)
    if not cover:
        raise HTTPException(status_code=404, detail="Cover not found.")
    return FileResponse(cover, media_type="image/png")


@router.get("/library/tracks/{artist}/{album}",
            tags=[tag],
            responses={404: {"description": "Album not found."}},
            response_model=TrackListModel)
async def get_tracks(artist: str, album: str):
    """
    Return a list of tracks for the specified album.
    """
    tracks = library.get_tracks(artist, album)
    if not tracks:
        raise HTTPException(status_code=404, detail="Album not found.")
    return {
        "artist":  artist,
        "album": album,
        "tracks": tracks}


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


@router.get("/library/path/album/{artist}/{album}",
            tags=[tag],
            responses={404: {"description": "Album not found."}},
            response_model=PathModel)
async def get_album_path(artist: str, album: str):
    """
    Return a path to the album specified.
    """
    album_path = library.get_path(artist, album)
    if not album_path:
        raise HTTPException(status_code=404, detail="Album not found.")
    return {"path":  album_path}


@router.get("/library/path/cover/{artist}/{album}",
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


@router.get("/library/search/{term}",
            tags=[tag],
            responses={404: {"description": "Match not found."}},
            response_model=SearchModel)
async def search(term: str):
    """
    Return an album that contains the given term in the artist name or album
    name (case insensitive).
    """
    match = library.search(term)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found.")
    return match
