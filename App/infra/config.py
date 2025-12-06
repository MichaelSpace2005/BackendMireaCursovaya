from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""

    class Config:
        extra = "ignore"
        env_file = ".env"
        case_sensitive = True
    
    # Database
    DB_USER: str = os.getenv("DATABASE_USER", os.getenv("DB_USER", "postgres"))
    DB_PASS: str = os.getenv("DATABASE_PASSWORD", os.getenv("DB_PASS", "postgres"))
    DB_HOST: str = os.getenv("DATABASE_HOST", os.getenv("DB_HOST", "localhost"))
    DB_PORT: int = int(os.getenv("DATABASE_PORT", os.getenv("DB_PORT", "5432")))
    DB_NAME: str = os.getenv("DATABASE_NAME", os.getenv("DB_NAME", "evolution_db"))

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    APP_NAME: str = "Evolution Tree API"
    VERSION: str = "1.0.0"

    @property
    def DATABASE_URL(self) -> str:
        """PostgreSQL connection URL"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
