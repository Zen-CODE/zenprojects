from fastapi import APIRouter, HTTPException
from routers.library.library_responses import ArtistListModel


router = APIRouter()


@router.get("/library/get_artists",
            tags=["Library"],
            responses={404: {"description": "Library folder not found."}},
            response_model=ArtistListModel)
async def get_artists():
    """
    Return a list of artists in the music library.
    """
    if False:
        raise HTTPException(status_code=404, detail="Library folder not found")
    return {"artists": ["artist1", "artists2"]}
