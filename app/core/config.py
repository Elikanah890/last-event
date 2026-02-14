# app/core/config.py
from pydantic import BaseSettings
from pathlib import Path

# Root project directory (Desktop/event-backend)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # go 3 levels up

class Settings(BaseSettings):
    # JWT / FastAPI
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 day

    # Database
    DATABASE_URL: str

    # Frontend invitation base URL
    INVITATION_BASE_URL: str = "https://yourfrontend.com/invitation"

    # Debug
    DEBUG: bool = False

    class Config:
        env_file = BASE_DIR / ".env"   # now points to Desktop/event-backend/.env
        env_file_encoding = "utf-8"

# Singleton settings
_settings: Settings | None = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
        print("✅ Loaded settings from .env")
        print(f"SECRET_KEY: {_settings.SECRET_KEY}")
        print(f"DATABASE_URL: {_settings.DATABASE_URL}")
    return _settings
