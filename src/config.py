from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent  # D:\code\charm\fapi\fasqlm
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,  # Явно указываем полный путь
        env_file_encoding="utf-8",
        extra="ignore",
    )
    DATABASE_URL: str

    TEST_DATABASE_URL: str
    JWT_SECRET : str
    JWT_ALGORITHM : str

Config = Settings()

# Проверка
#print("Does .env exist?", os.path.exists(ENV_PATH))  # True/False
#print(".env file path:", ENV_PATH)  # D:\code\charm\fapi\fasqlm\.env