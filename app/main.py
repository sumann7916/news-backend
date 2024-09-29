from fastapi import FastAPI, Depends
import uvicorn
from functools import lru_cache
from typing_extensions import Annotated
from app.config import Settings


app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/")
async def root(settings: Annotated[Settings, Depends(get_settings)]):
    return {"message": settings.POSTGRES_DB}
