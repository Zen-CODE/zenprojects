from fastapi import APIRouter

router = APIRouter()


@router.get("/library/get_artists", tags=["library"])
async def get_artists():
    return ["artist1", "artists2"]
