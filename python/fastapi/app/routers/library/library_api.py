from fastapi import APIRouter, HTTPException
from routers.library.library_responses import ArtisListModel


router = APIRouter()

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
