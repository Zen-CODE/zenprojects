from fastapi import FastAPI
from routers.library.library_api import router as library_router


app = FastAPI()
app.include_router(library_router)


@app.get("/")
async def zen_fast_api():
    return {"message": "Welcome to the Zen FASP API Media Server"}