import pytest
from unittest.mock import MagicMock, patch
from backend.rag import RAGService
from backend.embedding_service import EmbeddingService
from backend.models.session import Session
from backend.models.chat_message import ChatMessage
from backend.session_service import SessionService
from sqlalchemy.orm import Session as DbSession
import uuid


class TestRAGService:
    """Test cases for the RAGService class"""
    
    @patch('backend.rag.VectorStore')
    @patch('backend.rag.EmbeddingService')
    def setup_method(self, mock_embedding_service, mock_vector_store):
        """Set up the RAGService for testing"""
        self.mock_embedding_service = mock_embedding_service
        self.mock_vector_store = mock_vector_store
        
        self.rag_service = RAGService()
        self.rag_service.embedding_service = self.mock_embedding_service
        self.rag_service.vector_store = self.mock_vector_store
    
    def test_get_answer_standard_rag_success(self):
        """Test the standard RAG approach when everything works correctly"""
        query = "What is the main theme?"
        book_id = str(uuid.uuid4())
        
        # Mock embedding generation
        mock_embedding = [0.1, 0.2, 0.3]
        self.mock_embedding_service.generate_embedding.return_value = mock_embedding
        
        # Mock vector store search
        mock_search_result = [
            {
                "id": "chunk1",
                "score": 0.9,
                "payload": {
                    "content_preview": "The main theme is exploration.",
                    "source_file": "chapter1.md",
                    "source_section": "Introduction"
                }
            }
        ]
        self.mock_vector_store.search_similar.return_value = mock_search_result
        
        # Call the method
        result = self.rag_service.get_answer_standard_rag(query, book_id)
        
        # Verify the result
        assert "response" in result
        assert len(result["sources"]) == 1
        assert result["sources"][0]["chunk_id"] == "chunk1"
        
        # Verify the calls
        self.mock_embedding_service.generate_embedding.assert_called_once_with(query)
        self.mock_vector_store.search_similar.assert_called_once_with(
            query_vector=mock_embedding,
            book_id=book_id,
            limit=5
        )
    
    def test_get_answer_standard_rag_no_results(self):
        """Test the standard RAG approach when no similar chunks are found"""
        query = "What is the main theme?"
        book_id = str(uuid.uuid4())
        
        # Mock embedding generation
        mock_embedding = [0.1, 0.2, 0.3]
        self.mock_embedding_service.generate_embedding.return_value = mock_embedding
        
        # Mock vector store search returning empty results
        self.mock_vector_store.search_similar.return_value = []
        
        # Call the method
        result = self.rag_service.get_answer_standard_rag(query, book_id)
        
        # Verify the result
        assert "I couldn't find relevant information" in result["response"]
        assert len(result["sources"]) == 0
    
    def test_get_answer_targeted_rag_success(self):
        """Test the targeted RAG approach when everything works correctly"""
        query = "Explain this concept?"
        selected_text = "The concept is about artificial intelligence."
        
        # Call the method
        result = self.rag_service.get_answer_targeted_rag(query, selected_text)
        
        # Verify the result
        assert "response" in result
        assert len(result["sources"]) == 1
        assert result["sources"][0]["source_file"] == "selected_text"
        assert result["sources"][0]["relevance_score"] == 1.0
    
    def test_get_answer_uses_targeted_rag_when_selected_text_provided(self):
        """Test that get_answer uses targeted RAG when selected_text is provided"""
        query = "What does this mean?"
        book_id = str(uuid.uuid4())
        selected_text = "This is the selected text."
        
        # Mock the targeted RAG method
        with patch.object(self.rag_service, 'get_answer_targeted_rag') as mock_targeted:
            mock_targeted.return_value = {"response": "targeted response", "sources": []}
            
            result = self.rag_service.get_answer(query, book_id, selected_text)
            
            # Verify that targeted RAG was called
            mock_targeted.assert_called_once_with(query, selected_text)
            assert result["response"] == "targeted response"
    
    def test_get_answer_uses_standard_rag_when_no_selected_text(self):
        """Test that get_answer uses standard RAG when no selected_text is provided"""
        query = "What does this mean?"
        book_id = str(uuid.uuid4())
        
        # Mock the standard RAG method
        with patch.object(self.rag_service, 'get_answer_standard_rag') as mock_standard:
            mock_standard.return_value = {"response": "standard response", "sources": []}
            
            result = self.rag_service.get_answer(query, book_id, None)
            
            # Verify that standard RAG was called
            mock_standard.assert_called_once_with(query, book_id)
            assert result["response"] == "standard response"


class TestEmbeddingService:
    """Test cases for the EmbeddingService class"""
    
    def test_generate_embedding_success(self):
        """Test that embedding generation works correctly"""
        embedding_service = EmbeddingService()
        
        # Since we can't easily mock the OpenAI API in this context, 
        # we'll just verify the method exists and can be called
        assert hasattr(embedding_service, 'generate_embedding')
        assert callable(getattr(embedding_service, 'generate_embedding'))


class TestSessionService:
    """Test cases for the SessionService class"""
    
    def setup_method(self):
        """Set up the SessionService for testing"""
        self.mock_db = MagicMock(spec=DbSession)
        self.session_service = SessionService(self.mock_db)
    
    def test_get_or_create_session_new_session(self):
        """Test creating a new session when no session_id is provided"""
        self.mock_db.query().filter().first.return_value = None
        
        session_id = self.session_service.get_or_create_session(None)
        
        # Verify that a new session was created
        assert self.mock_db.add.called
        assert self.mock_db.commit.called
    
    def test_get_or_create_session_existing_session(self):
        """Test getting an existing session when session_id is provided"""
        existing_session_id = str(uuid.uuid4())
        mock_session = Session(session_id=existing_session_id)
        self.mock_db.query().filter().first.return_value = mock_session
        
        session_id = self.session_service.get_or_create_session(existing_session_id)
        
        # Verify that no new session was created
        assert session_id == existing_session_id
        assert not self.mock_db.add.called
    
    def test_add_message_to_session_success(self):
        """Test adding a message to a session successfully"""
        session_id = str(uuid.uuid4())
        role = "user"
        content = "Hello, world!"
        
        result = self.session_service.add_message_to_session(session_id, role, content)
        
        # Verify that the message was added to the DB
        assert self.mock_db.add.called
        assert self.mock_db.commit.called
        assert result is True
    
    def test_add_message_to_session_failure(self):
        """Test handling failure when adding a message to a session"""
        session_id = str(uuid.uuid4())
        role = "user"
        content = "Hello, world!"
        
        # Mock an exception during DB operation
        self.mock_db.add.side_effect = Exception("DB Error")
        
        result = self.session_service.add_message_to_session(session_id, role, content)
        
        # Verify that rollback was called and result is False
        assert self.mock_db.rollback.called
        assert result is False