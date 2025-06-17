from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str


Config = Settings()
