import os
import pathlib

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Task Tracker"
    region: str = os.getenv("REGION")
    access_key: str = os.getenv("ACCESS_KEY")
    secret_key: str = os.getenv("SECRET_KEY")
    bucket: str = os.getenv("BUCKET")

    class Config:
        env_file = f"{pathlib.Path(__file__).resolve().parent}/.env"


settings = Settings()
