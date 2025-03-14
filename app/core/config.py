import os
from pydantic_settings import BaseSettings
from pathlib import Path


# Use this to build paths inside the project
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Class to hold application's config values."""

    SECRET_KEY: str
    ALGORITHM: str
    ENVIRONMENT: str
    ACCESS_TOKEN_EXPIRY: int
    REFRESH_TOKEN_EXPIRY: int

    # Database configurations
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_TYPE: str

    # Directories
    MEDIA_DIR: str = os.path.join(BASE_DIR, "media")
    STATIC_DIR: str = os.path.join(BASE_DIR, "static")
    TEMPLATES_DIR: str = os.path.join(BASE_DIR, "templates")

    @property
    def database_url(self) -> str:
        """Dynamically construct DATABASE_URL"""
        return f"{self.DATABASE_TYPE}://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    class Config:
        env_file = ".env"


settings = Settings()
