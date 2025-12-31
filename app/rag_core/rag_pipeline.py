from typing import Dict, Any, List, Optional
import logging
from openai import AsyncOpenAI


class RAGPipeline:
    def __init__(self, openai_client: AsyncOpenAI, qdrant_client, postgres_client, config):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.postgres_client = postgres_client
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def process_query(self, question: str, selected_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a query through the RAG pipeline
        """
        try:
            # Generate embedding for the question
            embedding_response = await self.openai_client.embeddings.create(
                model=self.config.EMBEDDING_MODEL,
                input=question
            )
            question_embedding = embedding_response.data[0].embedding

            # Search for relevant documents in Qdrant
            search_results = await self.qdrant_client.search_vectors(
                query_vector=question_embedding,
                limit=5  # Get top 5 results
            )

            # Format context from search results
            context_texts = []
            source_citations = []
            for result in search_results:
                context_texts.append(result.payload.get("text", ""))
                source_citations.append(result.payload.get("source", "Unknown source"))

            # Combine context
            context = "\n".join(context_texts)
            
            # If there's selected context, add it to the main context
            if selected_context:
                context = f"Selected context: {selected_context}\n\nRelevant context: {context}"

            # Generate response using OpenAI
            response = await self.openai_client.chat.completions.create(
                model=self.config.CHAT_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context. If the answer is not in the context, say 'I don't know based on the provided information.'"},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}\n\nPlease provide a detailed answer based on the context, and include source citations where appropriate."}
                ],
                max_tokens=500
            )

            answer = response.choices[0].message.content

            return {
                "answer": answer,
                "source_citations": source_citations
            }
        except Exception as e:
            self.logger.error(f"Error in RAG pipeline: {e}")
            raise