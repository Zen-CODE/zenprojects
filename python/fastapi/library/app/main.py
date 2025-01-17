from fastapi import FastAPI
# AM I seeing this comment?
from .routers.library.library_api import router as library_router
from .routers.sound.sound_api import router as sound_router
from json import load


def get_tags_metadata():
    with open("tags_metadata.json", "rb") as f:
        return load(f)


app = FastAPI(
    title="ZenCODE Media Server",
    description="An experimental FastAPI Mediaplayer API for ZenPlayer",
    openapi_tags=get_tags_metadata(),
    docs_url="/swagger",
    redoc_url=None,
    version="0.0.1")


app.include_router(library_router)
app.include_router(sound_router)


@app.get("/")
async def zen_fast_api():
    return {"message": "Welcome to the Zen FAST API Media Server"}