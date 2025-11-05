from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Nova Corrente API"
    APP_VERSION: str = "3.0.0-postgres"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente")
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', 5432))
    DB_USER: str = os.getenv('DB_USER', 'nova_corrente')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'strong_password')
    DB_NAME: str = os.getenv('DB_NAME', 'nova_corrente')
    
    # API settings
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: str = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001')
    
    # Security settings
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'change-this-in-production')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 hours
    
    # External API settings (disabled in production)
    EXTERNAL_APIS_ENABLED: bool = os.getenv('EXTERNAL_APIS_ENABLED', 'false').lower() == 'true'
    ENABLE_ML_PROCESSING: bool = os.getenv('ENABLE_ML_PROCESSING', 'false').lower() == 'true'
    
    # Feature flags
    ENABLE_DEMAND_FORECASTING: bool = True
    ENABLE_INVENTORY_OPTIMIZATION: bool = True
    ENABLE_RECOMMENDATION_ENGINE: bool = True
    
    # Caching settings
    CACHE_DEFAULT_TIMEOUT: int = 300  # 5 minutes
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()