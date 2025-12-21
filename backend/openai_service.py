import openai
import logging
from typing import List, Dict, Any, Optional
from .config import settings


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY


class OpenAIService:
    def __init__(self):
        pass
    
    def generate_chat_completion(self, messages: List[Dict[str, str]], 
                                 model: str = "gpt-4o", 
                                 temperature: float = 0.7,
                                 max_tokens: int = 1000) -> Optional[str]:
        """
        Generate a chat completion using OpenAI's API.
        
        Args:
            messages: List of messages in the conversation (role and content)
            model: The model to use for completion
            temperature: Controls randomness in the response
            max_tokens: Maximum number of tokens in the response
            
        Returns:
            Generated response text or None if an error occurs
        """
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error generating chat completion: {e}")
            return None
    
    def generate_streaming_chat_completion(self, messages: List[Dict[str, str]], 
                                           model: str = "gpt-4o", 
                                           temperature: float = 0.7,
                                           max_tokens: int = 1000):
        """
        Generate a streaming chat completion using OpenAI's API.
        
        Args:
            messages: List of messages in the conversation (role and content)
            model: The model to use for completion
            temperature: Controls randomness in the response
            max_tokens: Maximum number of tokens in the response
            
        Yields:
            Response chunks as they are generated
        """
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            logger.error(f"Error generating streaming chat completion: {e}")
            yield "Sorry, I encountered an error while generating a response."