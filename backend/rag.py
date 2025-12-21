from typing import List, Dict, Any, Optional
from .vector_store import VectorStore
from .embedding_service import EmbeddingService
from .config import settings
import logging
import openai
import uuid


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY


class RAGService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.embedding_service = EmbeddingService()
    
    def _generate_response(self, query: str, context: str, selected_text: Optional[str] = None) -> str:
        """
        Generate a response using OpenAI based on the provided context.
        
        Args:
            query: User's query
            context: Context to use for answering the query
            selected_text: Optional selected text that takes priority
            
        Returns:
            Generated response
        """
        try:
            # Use selected text as primary context if provided
            if selected_text:
                primary_context = f"Selected text: {selected_text}\n\n"
            else:
                primary_context = ""
            
            # Prepare the system message to guide the AI's behavior
            system_message = f"""You are an AI assistant for the book '{settings.APP_NAME}'. 
            Use the provided context to answer the user's query. 
            If the user has selected specific text, prioritize that text above all else in your response.
            If the information is not available in the provided context, say so clearly.
            Always be helpful and accurate based on the provided information."""
            
            # Prepare the user message with context
            user_message = f"""Context: {primary_context}{context}

            Query: {query}

            Please provide a helpful and accurate response based on the context provided."""
            
            # Call OpenAI API to generate the response
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error while generating a response. Please try again later."
    
    def get_answer_standard_rag(self, query: str, book_id: str) -> Dict[str, Any]:
        """
        Get answer using standard RAG approach (vector search in Qdrant).
        
        Args:
            query: User's query
            book_id: ID of the book to search in
            
        Returns:
            Dictionary containing response and sources
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_service.generate_embedding(query)
            
            if not query_embedding:
                logger.error("Failed to generate embedding for the query")
                return {
                    "response": "Sorry, I couldn't process your query. Please try again.",
                    "sources": []
                }
            
            # Search for similar chunks in the vector store
            similar_chunks = self.vector_store.search_similar(
                query_vector=query_embedding,
                book_id=book_id,
                limit=5  # Retrieve top 5 similar chunks
            )
            
            if not similar_chunks:
                logger.info("No similar chunks found for the query")
                return {
                    "response": "I couldn't find relevant information to answer your query.",
                    "sources": []
                }
            
            # Build context from the retrieved chunks
            context_parts = []
            sources = []
            
            for chunk in similar_chunks:
                # Add the content to context
                content = chunk["payload"]["content_preview"]  # In production, fetch full content from DB
                context_parts.append(content)
                
                # Add source information
                sources.append({
                    "chunk_id": chunk["id"],
                    "content": content,
                    "source_file": chunk["payload"]["source_file"],
                    "source_section": chunk["payload"].get("source_section", ""),
                    "relevance_score": chunk["score"]
                })
            
            context = "\n\n".join(context_parts)
            
            # Generate the response using the context
            response = self._generate_response(query, context)
            
            return {
                "response": response,
                "sources": sources
            }
        
        except Exception as e:
            logger.error(f"Error in standard RAG: {e}")
            return {
                "response": "Sorry, I encountered an error while processing your query. Please try again later.",
                "sources": []
            }
    
    def get_answer_targeted_rag(self, query: str, selected_text: str) -> Dict[str, Any]:
        """
        Get answer using targeted RAG approach (context from selected text).
        
        Args:
            query: User's query
            selected_text: Text selected by the user to use as context
            
        Returns:
            Dictionary containing response and sources
        """
        try:
            # Generate the response using the selected text as primary context
            response = self._generate_response(query, selected_text, selected_text=selected_text)
            
            # For targeted RAG, we only have the selected text as context
            sources = [{
                "chunk_id": f"selected_text_{uuid.uuid4()}",
                "content": selected_text[:500] + "..." if len(selected_text) > 500 else selected_text,  # Preview
                "source_file": "selected_text",
                "source_section": "user_selection",
                "relevance_score": 1.0  # Highest relevance since it's the primary context
            }]
            
            return {
                "response": response,
                "sources": sources
            }
        
        except Exception as e:
            logger.error(f"Error in targeted RAG: {e}")
            return {
                "response": "Sorry, I encountered an error while processing your query. Please try again later.",
                "sources": []
            }
    
    def get_answer(self, query: str, book_id: str, selected_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Get answer using either standard RAG or targeted RAG based on selected_text.
        
        Args:
            query: User's query
            book_id: ID of the book to search in
            selected_text: Optional selected text that takes priority
            
        Returns:
            Dictionary containing response and sources
        """
        if selected_text:
            # Use targeted RAG approach
            logger.info("Using targeted RAG approach with selected text")
            return self.get_answer_targeted_rag(query, selected_text)
        else:
            # Use standard RAG approach
            logger.info("Using standard RAG approach with vector search")
            return self.get_answer_standard_rag(query, book_id)