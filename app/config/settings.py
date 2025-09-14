import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "test")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # App
    app_name: str = "Đồ án môn học Python - Web API"
    app_version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")

    # CORS
    allowed_hosts: list = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
