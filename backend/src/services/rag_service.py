from typing import List, Dict, Any
from ..core.qdrant import qdrant_service
from ..services.embedding_service import embedding_service
from ..core.logging import app_logger
from openai import OpenAI
from dotenv import load_dotenv
from ..core.config import settings

load_dotenv()

class RAGService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.CHAT_MODEL

    def query_rag(self, question: str, selected_text: str = None, top_k: int = 5) -> Dict[str, Any]:
        """
        Perform RAG query with the given question
        If selected_text is provided, use it as additional context
        """
        try:
            # Generate embedding for the question
            query_embedding = embedding_service.generate_embedding(question)
            
            # Search in Qdrant for relevant chunks
            search_results = qdrant_service.search_vectors(
                query_vector=query_embedding,
                limit=top_k
            )
            
            # Prepare context from search results
            context_parts = []
            sources = []
            
            for result in search_results:
                payload = result["payload"]
                context_parts.append(payload["content"])
                sources.append({
                    "url": payload.get("source_url", ""),
                    "heading": payload.get("heading", ""),
                    "content": payload["content"][:200] + "..." if len(payload["content"]) > 200 else payload["content"]
                })
            
            # Combine context
            context = "\n\n".join(context_parts)
            
            # If selected text is provided, add it to the context
            if selected_text:
                context = f"Selected text context: {selected_text}\n\nRelevant information from the book:\n{context}"
            
            # Generate response using OpenAI
            prompt = f"""
            Based on the following context, please answer the question. 
            If the context doesn't contain enough information to answer the question, 
            please say so clearly.
            
            Context:
            {context}
            
            Question: {question}
            
            Answer:
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context. Always cite the source of information when possible."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "sources": sources,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            app_logger.error(f"Error in RAG query: {str(e)}")
            # Return a graceful response when external services are unavailable
            return {
                "answer": "I'm having trouble accessing the book content right now. Please try again later.",
                "sources": [],
                "tokens_used": 0
            }

    def query_global(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Perform a global RAG query without specific context
        """
        return self.query_rag(question, selected_text=None, top_k=top_k)

    def query_with_context(self, question: str, selected_text: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Perform a RAG query with selected text as context
        """
        return self.query_rag(question, selected_text=selected_text, top_k=top_k)


# Global instance
rag_service = RAGService()