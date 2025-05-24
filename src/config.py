from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    JWT_SECRET : str
    JWT_ALGORITHM : str


Config = Settings()
