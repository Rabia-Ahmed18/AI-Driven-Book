import asyncpg
import logging
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class PostgresClient:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def connect(self):
        """
        Establish connection to the database
        """
        try:
            self.pool = await asyncpg.create_pool(
                dsn=self.database_url,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            logger.info("Connected to PostgreSQL database")
            
            # Create required tables if they don't exist
            await self._create_tables()
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            raise

    async def _create_tables(self):
        """
        Create required tables if they don't exist
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS vector_metadata (
            chunk_id VARCHAR(255) PRIMARY KEY,
            source_file VARCHAR(500) NOT NULL,
            source_section VARCHAR(500),
            content_text TEXT,
            embedding_id VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(create_table_query)
                logger.info("Ensured vector_metadata table exists")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise

    async def save_metadata(self, chunk_id: str, source_file: str, source_section: Optional[str], 
                           content_text: str, embedding_id: str) -> bool:
        """
        Save metadata for a text chunk to the database
        """
        try:
            insert_query = """
            INSERT INTO vector_metadata (chunk_id, source_file, source_section, content_text, embedding_id)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (chunk_id) DO UPDATE SET
                source_file = EXCLUDED.source_file,
                source_section = EXCLUDED.source_section,
                content_text = EXCLUDED.content_text,
                embedding_id = EXCLUDED.embedding_id,
                updated_at = CURRENT_TIMESTAMP
            """
            
            async with self.pool.acquire() as conn:
                await conn.execute(
                    insert_query,
                    chunk_id, source_file, source_section, content_text, embedding_id
                )
                
            logger.info(f"Saved metadata for chunk {chunk_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving metadata for chunk {chunk_id}: {e}")
            return False

    async def get_metadata(self, chunk_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieve metadata for a list of chunk IDs
        """
        try:
            query = """
            SELECT chunk_id, source_file, source_section
            FROM vector_metadata
            WHERE chunk_id = ANY($1)
            """
            
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query, chunk_ids)
                
            results = []
            for row in rows:
                results.append({
                    'chunk_id': row['chunk_id'],
                    'source_file': row['source_file'],
                    'source_section': row['source_section']
                })
                
            return results
        except Exception as e:
            logger.error(f"Error retrieving metadata: {e}")
            return []

    async def close(self):
        """
        Close the database connection pool
        """
        if self.pool:
            await self.pool.close()
            logger.info("Closed PostgreSQL connection pool")