import openai
import logging
from typing import List, Optional
from .config import settings


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY


class EmbeddingService:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a single text"""
        try:
            # Ensure the text is within the model's token limit
            # The text-embedding-3-small model can handle up to 8191 tokens
            # For safety, we'll limit to 7000 tokens which is roughly 5000-6000 words
            if len(text) > 20000:  # Rough estimate of character limit
                logger.warning(f"Text is very long ({len(text)} chars), consider truncating for embedding generation")
                # Truncate to a reasonable length
                text = text[:20000]
            
            response = openai.embeddings.create(
                input=text,
                model=self.model
            )
            
            # Extract the embedding from the response
            embedding = response.data[0].embedding
            return embedding
        
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def generate_embeddings_batch(self, texts: List[str]) -> Optional[List[List[float]]]:
        """Generate embeddings for a batch of texts"""
        try:
            # The OpenAI API allows up to 2048 texts per request
            # For safety, we'll limit to 100 per batch
            batch_size = min(100, len(texts))
            all_embeddings = []
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                # Ensure texts are within reasonable length
                processed_batch = []
                for text in batch:
                    if len(text) > 20000:  # Rough estimate of character limit
                        logger.warning(f"Text is very long ({len(text)} chars), consider truncating for embedding generation")
                        text = text[:20000]
                    processed_batch.append(text)
                
                response = openai.embeddings.create(
                    input=processed_batch,
                    model=self.model
                )
                
                # Extract embeddings from the response
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
            
            return all_embeddings
        
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return None