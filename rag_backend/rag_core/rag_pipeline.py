import logging
import asyncio
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from .qdrant_client import QdrantClientWrapper
from .postgres_client import PostgresClient

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, openai_client: AsyncOpenAI, qdrant_client: QdrantClientWrapper, postgres_client: PostgresClient, config):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client
        self.postgres_client = postgres_client
        self.config = config
        self.timeout = 30  # 30 seconds timeout for operations

    async def generate_embeddings(self, text_chunks: List[str]) -> List[List[float]]:
        """
        Generate embeddings for text chunks using OpenAI
        """
        try:
            response = await self.openai_client.embeddings.create(
                input=text_chunks,
                model=self.config.embedding_model
            )
            
            embeddings = [item.embedding for item in response.data]
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    async def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from Qdrant based on the query
        """
        try:
            # Generate embedding for the query
            query_embedding = await self.generate_embeddings([query])
            
            # Search in Qdrant
            search_results = await self.qdrant_client.search(
                query_vector=query_embedding[0],
                top_k=top_k
            )
            
            # Retrieve metadata for the results
            chunk_ids = [result['id'] for result in search_results]
            metadata = await self.postgres_client.get_metadata(chunk_ids)
            
            # Combine search results with metadata
            full_contexts = []
            for result, meta in zip(search_results, metadata):
                full_contexts.append({
                    'id': result['id'],
                    'payload': result['payload'],
                    'score': result['score'],
                    'source_file': meta.get('source_file', ''),
                    'source_section': meta.get('source_section', '')
                })
                
            return full_contexts
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            raise

    async def generate_response(self, question: str, context: str, selected_context: Optional[str] = None) -> str:
        """
        Generate response using OpenAI based on the provided context
        """
        try:
            # If selected context is provided, prioritize it over retrieved context
            if selected_context:
                final_context = f"Please answer based only on the following selected text: {selected_context}. Question: {question}"
            else:
                final_context = f"Please answer based only on the following context: {context}. Question: {question}"
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # Consider using gpt-4 if more accuracy is needed
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Answer based only on the provided context. If the answer is not in the context, say 'I cannot answer based on the provided context.'"
                    },
                    {
                        "role": "user",
                        "content": final_context
                    }
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    async def process_query(self, question: str, selected_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Main method to process a query through the RAG pipeline
        """
        try:
            # If selected context is provided, use it directly
            if selected_context:
                logger.info("Using selected context for query processing")
                
                # Generate response with selected context only
                answer = await self.generate_response(
                    question=question,
                    context=selected_context,
                    selected_context=None  # Already included in context
                )
                
                # Return answer with empty citations since we're using provided context
                return {
                    "answer": answer,
                    "source_citations": []
                }
            else:
                # Use general flow with Qdrant retrieval
                logger.info("Using general RAG flow for query processing")
                
                # Retrieve relevant context from Qdrant
                retrieved_contexts = await self.retrieve_context(
                    query=question,
                    top_k=self.config.top_k_chunks
                )
                
                # Combine retrieved contexts
                combined_context = "\n\n".join([ctx['payload'].get('content', '') for ctx in retrieved_contexts])
                
                # Generate response using both question and retrieved context
                answer = await self.generate_response(
                    question=question,
                    context=combined_context
                )
                
                # Extract source citations
                source_citations = [f"{ctx['source_file']}#{ctx['source_section']}" for ctx in retrieved_contexts]
                
                return {
                    "answer": answer,
                    "source_citations": source_citations
                }
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise