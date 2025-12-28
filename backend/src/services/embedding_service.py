import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from ..core.config import settings
from ..core.logging import app_logger

load_dotenv()

class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using OpenAI's embedding API
        """
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            
            embeddings = []
            for item in response.data:
                embeddings.append(item.embedding)
            
            return embeddings
        except Exception as e:
            app_logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        return self.generate_embeddings([text])[0]

    def get_embedding_dimensions(self) -> int:
        """
        Get the expected dimensions for embeddings
        For text-embedding-3-small, this is 1536
        """
        if self.model == "text-embedding-3-small":
            return 1536
        elif self.model == "text-embedding-ada-002":
            return 1536
        elif self.model == "text-embedding-3-large":
            return 3072
        else:
            # Default to 1536 for most OpenAI embedding models
            return 1536


# Global instance
embedding_service = EmbeddingService()