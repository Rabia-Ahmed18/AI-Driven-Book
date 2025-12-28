from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    # OpenAI Settings
    OPENAI_API_KEY: str
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHAT_MODEL: str = "gpt-4-turbo"

    # Qdrant Settings
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION_NAME: str = "book_chunks"

    # Security
    SECRET_KEY: str
    ALLOWED_ORIGINS: List[str] = ["*"]  # Should be configured properly for production

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100  # requests per minute
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # Frontend Configuration (added to prevent validation errors)
    REACT_APP_API_BASE_URL: str = "http://localhost:8000"
    REACT_APP_CHATBOT_ENABLED: str = "true"

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in .env that aren't defined in the model


settings = Settings()