from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    
    # Qdrant settings
    QDRANT_URL: str
    QDRANT_API_KEY: Optional[str] = None
    
    # OpenAI settings
    OPENAI_API_KEY: str
    
    # Application settings
    APP_NAME: str = "RAG-Based AI Book Chatbot"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"


settings = Settings()