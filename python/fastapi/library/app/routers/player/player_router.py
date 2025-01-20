from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
from routers.player.player_responses import StateModel, MetaDataModel
from routers.player.player import ZenPlayerController


router = APIRouter()
tag = "Player"


@router.get("/player/get_state",
            tags=[tag],
            responses={404: {"description": "ZenPlayer not found."}},
            response_model=StateModel)
async def get_state():
    """
    The the state and details of the currently playing track.
    """
    # artists = library.get_artists()
    # if not artists:
    #     raise HTTPException(status_code=404, detail="Library folder not found")
    # return {"artists": artists}
    return ZenPlayerController.get_state()


@router.get("/player/get_track_meta",
            tags=[tag],
            responses={404: {"description": "ZenPlayer not found."}},
            response_model=MetaDataModel)
async def get_track_meta():
    """
    Return the technical details of the currently playing file.
    """
    return ZenPlayerController.get_track_meta()
