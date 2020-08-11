from fastapi import APIRouter, HTTPException
# from routers.library.library_responses import (
#     ArtistListModel, AlbumListModel, AlbumModel, PathModel, TrackListModel,
#     SearchModel)
# from components.library import Library
from starlette.responses import FileResponse
from components.sound_vlc import Sound
from os.path import exists


router = APIRouter()
sound = Sound()
tag = "Sound"


@router.get("/sound/play",
            tags=[tag],
            responses={404: {"description": "Audio file not found."}})
async def play(filename: str):
    """ Play the specified audio file. """

    if not exists(filename):
        raise HTTPException(status_code=404, detail="Audio not found")

    Sound.play(filename)
    return {"message": "success"}


@router.get("/sound/stop",
            tags=[tag])
async def stop():
    """ Stop any playing audio. """
    Sound.stop()
    return {"message": "success"}


@router.get("/sound/pause",
            tags=[tag])
async def pause():
    """ Stop any playing audio. """
    Sound.pause()
    return {"message": "success"}


@router.get("/sound/volume",
            tags=[tag])
async def set_volume(volume: float):
    """ Set the volume to between 0 (silent) and 1.0 (maximum). """
    Sound.set_volume(volume)
    return {"message": "success"}


@router.get("/sound/position",
            tags=[tag])
async def set_position(position: float):
    """ Set the positon to between 0 (start) and 1.0 (end). """
    Sound.set_position(position)
    return {"message": "success"}
