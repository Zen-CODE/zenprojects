from fastapi import FastAPI
from routers import library


app = FastAPI()
app.include_router(library.router)


@app.get("/")
async def zen_fast_api():
    return {"message": "Welcome to the Zen FASP API Media Server"}