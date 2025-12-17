from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # OpenAI Configuration
    GEMINI_API_KEY: str= "AIzaSyBvkNR_ZW0s2lISWzlGsePmTJNuGGUsTHU"
    
    # Qdrant Configuration
    qdrant_url:str="https://1c8b71c7-3495-484e-91c6-dfd14721cb76.europe-west3-0.gcp.cloud.qdrant.io:6333"
    qdrant_api_key:str="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.6VMO-_69POcyRfZfyeRD-fTQdWmXpctdA8sNY5HSOLY"
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    
    # Neon Postgres Configuration
    neon_database_url: str='postgresql://neondb_owner:npg_QW3UdAgbi1Ih@ep-hidden-paper-a4h1dd80-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
    
    # Application Configuration
    log_level: str = "INFO"
    
    # RAG Configuration
    top_k_chunks: int = 5
    embedding_model: str = "text-embedding-3-small"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a single instance of settings
settings = Settings()