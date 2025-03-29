import os
from pydantic_settings import BaseSettings
from functools import lru_cache

def get_project_id() -> str:
    return os.getenv("PROJECT_ID", "hackfest-vertex-ai")

class Settings(BaseSettings):
    PROJECT_ID:str="hackfest-vertex-ai"

    # TTS Settings
    TTS_LANGUAGE_CODE: str = "id-ID"
    TTS_SPEAKING_RATE: float = 1.2
    TTS_PITCH: float = 3.0
    TTS_GENDER: str = "FEMALE"

    # Database Settings
    DB_USER: str = "xxx"
    DB_PASSWORD: str = "xxxx"
    DB_HOST: str = "10.xxx.xx.xx"
    DB_PORT: str = "5432"
    DB_NAME: str = "hansel_test"

    # API Keys
    GOOGLE_MAP_API_KEY: str = ""
    GOOGLE_APPLICATION_CREDENTIALS : str = "app/secrets/service-account.json"

    @property
    def DATABASE_URL(self) -> str:
        """Construct database connection string."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = "./app/.env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()