from fastapi import FastAPI

lights_api = FastAPI()

@lights_api.get("/")
async def read_root():
    return("Wahoo!")