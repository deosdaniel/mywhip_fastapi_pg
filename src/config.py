import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_ENV_PATH = BASE_DIR / ".env"
ENV_PATH = Path(os.environ.get("ENV_FILE", DEFAULT_ENV_PATH))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    TESTING: bool = False


Config = Settings()

IS_TEST_ENV = Config.TESTING
