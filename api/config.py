from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = "http://127.0.0.1:8000"

    DATABASE_URI: str = "sqlite:///./database.db"

    SALT: str = "test"
    MIN_LENGTH: int = 6

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
