from pydantic_settings import BaseSettings
from pydantic import Field
import os
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Voice AI Studio"
    APP_ENV: str = "development"
    DEBUG: bool = True

    API_HOST: str = "127.0.0.1"
    API_PORT: int = 3900

    DATA_DIR: Path = Path("./data")

    DATABASE_URL: str = "sqlite:///./data/database.sqlite"

    CUDA_ENABLED: bool = True
    MPS_ENABLED: bool = True
    ROCM_ENABLED: bool = True

    DEFAULT_TTS_ENGINE: str = "piper"
    DEFAULT_ASR_ENGINE: str = "faster-whisper"

    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "voice-ai-studio-secret-key-change-in-production"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

os.makedirs(settings.DATA_DIR / "voices", exist_ok=True)
os.makedirs(settings.DATA_DIR / "models", exist_ok=True)
os.makedirs(settings.DATA_DIR / "projects", exist_ok=True)
os.makedirs(settings.DATA_DIR / "audio", exist_ok=True)
os.makedirs(settings.DATA_DIR / "video", exist_ok=True)
os.makedirs(settings.DATA_DIR / "jobs", exist_ok=True)
os.makedirs(settings.DATA_DIR / "cache", exist_ok=True)
os.makedirs(settings.DATA_DIR / "logs", exist_ok=True)
