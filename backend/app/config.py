"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "5000"))
    API_RELOAD: bool = os.getenv("API_RELOAD", "false").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/nova_corrente.db")
    
    # ML Models
    MODELS_DIR: str = os.getenv("MODELS_DIR", "./models")
    MODEL_CACHE_ENABLED: bool = os.getenv("MODEL_CACHE_ENABLED", "true").lower() == "true"
    MODEL_CACHE_TTL: int = int(os.getenv("MODEL_CACHE_TTL", "3600"))
    
    # Data
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    RAW_DATA_DIR: str = os.getenv("RAW_DATA_DIR", "./data/raw")
    PROCESSED_DATA_DIR: str = os.getenv("PROCESSED_DATA_DIR", "./data/processed")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "./logs")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS - use string default and parse with validator
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://localhost:3001"
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS_ORIGINS from string or list"""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Split by comma and strip whitespace
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        # Default fallback
        return ["http://localhost:3000", "http://localhost:3001"]
    
    # Frontend
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Don't fail if .env doesn't exist or has parsing errors
        extra = "ignore"


# Try to load settings, but use defaults if .env has issues
try:
    settings = Settings()
except Exception as e:
    # If .env parsing fails, use environment variables with defaults
    print(f"Warning: Could not load settings from .env: {e}")
    print("Using default environment variables...")
    
    class FallbackSettings:
        """Fallback settings using only environment variables"""
        API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
        API_PORT: int = int(os.getenv("API_PORT", "5000"))
        API_RELOAD: bool = os.getenv("API_RELOAD", "false").lower() == "true"
        DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/nova_corrente.db")
        MODELS_DIR: str = os.getenv("MODELS_DIR", "./models")
        MODEL_CACHE_ENABLED: bool = os.getenv("MODEL_CACHE_ENABLED", "true").lower() == "true"
        MODEL_CACHE_TTL: int = int(os.getenv("MODEL_CACHE_TTL", "3600"))
        DATA_DIR: str = os.getenv("DATA_DIR", "./data")
        RAW_DATA_DIR: str = os.getenv("RAW_DATA_DIR", "./data/raw")
        PROCESSED_DATA_DIR: str = os.getenv("PROCESSED_DATA_DIR", "./data/processed")
        LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        LOG_DIR: str = os.getenv("LOG_DIR", "./logs")
        SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")
        ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",") if os.getenv("CORS_ORIGINS") else ["http://localhost:3000", "http://localhost:3001"]
        FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    settings = FallbackSettings()

