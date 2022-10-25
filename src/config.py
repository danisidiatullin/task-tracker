from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Task Tracker"
    region: str
    access_key: str
    secret_key: str
    bucket: str

    class Config:
        env_file = ".env"


settings = Settings()
