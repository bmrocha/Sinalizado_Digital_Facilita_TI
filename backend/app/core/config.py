"""
Configuration settings for the Digital Signage API
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator

class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_V1_STR: str = "/api/v1"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./digital_signage.db"

    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if v.startswith("sqlite"):
            # Ensure SQLite database directory exists
            db_path = v.replace("sqlite:///", "")
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return v

    # JWT Configuration
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload Configuration
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 104857600  # 100MB

    # CORS Origins
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    # Raspberry Pi Configuration
    RASPBERRY_PI_DEFAULT_ORIENTATION: str = "horizontal"
    HIBERNATION_ENABLED: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
