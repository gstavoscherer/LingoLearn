from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "../.env"

class Settings(BaseSettings):
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    FRONTEND_URL: str
    DATABASE_URL: str
    JWT_KEY: str
    JWT_ALGORITHM: str
    API_PORT: int = 8000
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ENV_PATH
        env_file_encoding = 'utf-8'

settings = Settings()
