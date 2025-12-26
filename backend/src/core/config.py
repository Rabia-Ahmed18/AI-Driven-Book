from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Configuration
    neon_database_url: str
    
    # Vector Database Configuration
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "book_chunks"
    
    # OpenAI Configuration
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4-turbo"

    # Application Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    secret_key: str = "dev-secret-key-for-development"  # Default for development
    
    # Rate limiting
    requests_per_minute: int = 60

    class Config:
        env_file = ".env"


settings = Settings()