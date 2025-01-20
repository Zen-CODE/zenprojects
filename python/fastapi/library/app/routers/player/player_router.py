from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
from routers.player.player_responses import StateModel


router = APIRouter()
# library = Library()
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
    return {
        "album": "My album",
        "artist": "My artist",
        "cover": "",
        "file_name": "My filename",
        "position": 25,
        "state": "PLaying",
        "time_display": "Dispaly here",
        "track" : 1,
        "volume": 50
    }
