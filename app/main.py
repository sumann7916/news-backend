from fastapi import FastAPI, Depends
import uvicorn
from functools import lru_cache
from typing_extensions import Annotated
from app.config import SettingsManager


app = FastAPI()


@app.get("/")
async def root():
    settings = SettingsManager.get_settings()
    return {"message": settings.POSTGRES_DB}
