from fastapi import FastAPI
from routers.library.library_api import router as library_router
from json import load


def get_tags_metadata():
    with open("tags_metadata.json", "rb") as f:
        return load(f)


app = FastAPI(
    title="ZenCODE Media Server",
    description="An experimental FastAPI Mediaplayer API for ZenPlayer",
    openapi_tags=get_tags_metadata(),
    version="0.0.1")


app.include_router(library_router)

@app.get("/")
async def zen_fast_api():
    return {"message": "Welcome to the Zen FASP API Media Server"}