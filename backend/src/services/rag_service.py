from typing import List, Dict, Any
from uuid import UUID
import uuid
from openai import AsyncOpenAI
from ..core.config import settings
from ..core.vector_store import vector_store
from ..models.interaction import Citation


class RAGService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def get_global_context_response(self, query: str, book_id: str) -> Dict[str, Any]:
        """
        Get response based on global context (entire book)
        """
        # Generate embedding for the query
        response = await self.openai_client.embeddings.create(
            input=query,
            model=settings.embedding_model
        )
        query_embedding = response.data[0].embedding
        
        # Search in vector store for relevant chunks
        search_results = vector_store.search(
            query_vector=query_embedding,
            book_id=book_id,
            limit=5  # Get top 5 relevant chunks
        )
        
        # Prepare context from search results
        context_parts = []
        citations = []
        for result in search_results:
            if result.score > 0.5:  # Only include results with sufficient similarity
                context_parts.append(result.payload.get("content", ""))
                citations.append(
                    Citation(
                        chunk_id=result.id,
                        text=result.payload.get("content", "")[:200] + "...",  # First 200 chars
                        confidence=result.score,
                        metadata=result.payload.get("metadata", {})
                    )
                )
        
        context = "\n\n".join(context_parts)
        
        # Generate response using OpenAI
        messages = [
            {"role": "system", "content": f"You are a helpful assistant that answers questions based on the provided book content. Use the following context from the book to answer the user's question. If you cannot answer based on the context, say so. Context: {context}"},
            {"role": "user", "content": query}
        ]
        
        completion = await self.openai_client.chat.completions.create(
            model=settings.chat_model,
            messages=messages,
            max_tokens=500
        )
        
        response_text = completion.choices[0].message.content
        
        return {
            "response": response_text,
            "citations": citations
        }
    
    async def get_selection_context_response(self, query: str, selected_text: str, book_id: str) -> Dict[str, Any]:
        """
        Get response based on selection context (only the selected text)
        """
        # For selection context, we directly use the selected text as context
        context = selected_text
        
        # Generate response using OpenAI with the selected text as context
        messages = [
            {"role": "system", "content": f"You are a helpful assistant that answers questions based only on the provided selected text. Use ONLY the following selected text to answer the user's question. Do not use any other knowledge. Selected text: {context}"},
            {"role": "user", "content": query}
        ]
        
        completion = await self.openai_client.chat.completions.create(
            model=settings.chat_model,
            messages=messages,
            max_tokens=500
        )
        
        response_text = completion.choices[0].message.content
        
        # Create a citation for the selected text
        citation = Citation(
            chunk_id=str(uuid.uuid4()),
            text=selected_text[:200] + "...",  # First 200 chars
            confidence=1.0,  # High confidence since it's direct context
            metadata={"source": "selected_text", "book_id": book_id}
        )
        
        return {
            "response": response_text,
            "citations": [citation]
        }