from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

def get_env_files():

    files = [".env"]  # Basis immer laden

    ENV = os.getenv("ENVIRONMENT", "development")
    if ENV == "production":
        files.append(".env.production")
    elif ENV == "development":
        files.append(".env.development")

    return files

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=get_env_files(),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    utils_base_url: str = "http://localhost:8002/"

settings = Settings()
