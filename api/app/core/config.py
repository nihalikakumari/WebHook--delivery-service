from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Webhook Delivery Service"
    PROJECT_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # CORS - Allow all origins in production, will be restricted by Render's proxy
    CORS_ORIGINS: List[str] = ["*"]
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "webhook_service"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/webhook_service"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Webhook Settings
    MAX_RETRY_ATTEMPTS: int = 5
    INITIAL_RETRY_DELAY: int = 10  # seconds
    MAX_RETRY_DELAY: int = 900  # 15 minutes
    DELIVERY_TIMEOUT: int = 10  # seconds
    LOG_RETENTION_DAYS: int = 3

    # JWT Settings
    SECRET_KEY: str = "your-secret-key"  # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()