from fastapi import APIRouter, HTTPException
from ...components.sound_vlc import Sound
from os.path import exists
from ...routers.sound.sound_responses import SoundStateModel


router = APIRouter()
sound = Sound()
tag = "Sound"


@router.post("/sound/play",
             tags=[tag],
             responses={404: {"description": "Audio file not found."}},
             response_model=SoundStateModel)
async def play(filename: str):
    """ Play the specified audio file. """

    if not exists(filename):
        raise HTTPException(status_code=404, detail="Audio not found")

    Sound.play(filename)
    return Sound.get_state()


@router.post("/sound/stop",
             tags=[tag],
             response_model=SoundStateModel)
async def stop():
    """ Stop any playing audio. """
    Sound.stop()
    return Sound.get_state()


@router.post("/sound/pause",
             tags=[tag],
             response_model=SoundStateModel)
async def pause():
    """ Stop any playing audio. """
    Sound.pause()
    return Sound.get_state()


@router.post("/sound/volume",
             tags=[tag],
             response_model=SoundStateModel)
async def set_volume(volume: float):
    """ Set the volume to between 0 (silent) and 1.0 (maximum). """
    Sound.set_volume(volume)
    return Sound.get_state()


@router.post("/sound/position",
             tags=[tag],
             response_model=SoundStateModel)
async def set_position(position: float):
    """ Set the positon to between 0 (start) and 1.0 (end). """
    Sound.set_position(position)
    return Sound.get_state()


@router.get("/sound/state",
            tags=[tag],
            response_model=SoundStateModel)
async def get_state():
    """ Get the player state. """
    return Sound.get_state()
