import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.main import app
from backend.rag import RAGService
import json


client = TestClient(app)


class TestAPIEndpoints:
    """Integration tests for the API endpoints"""
    
    @patch('backend.routers.chat.rag_service')
    def test_chat_endpoint_success(self, mock_rag_service):
        """Test the chat endpoint with a successful response"""
        # Mock the RAG service response
        mock_response = {
            "response": "This is the AI response",
            "sources": [
                {
                    "chunk_id": "test_chunk_id",
                    "content": "Test content",
                    "source_file": "test.md",
                    "relevance_score": 0.9
                }
            ]
        }
        mock_rag_service.get_answer.return_value = mock_response
        
        # Prepare the request payload
        payload = {
            "query": "What is the main theme?",
            "book_id": "test-book-id"
        }
        
        # Make the request
        response = client.post("/api/v1/chat", json=payload)
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "This is the AI response"
        assert len(data["sources"]) == 1
        assert data["sources"][0]["chunk_id"] == "test_chunk_id"
    
    @patch('backend.routers.chat.rag_service')
    def test_chat_endpoint_with_selected_text(self, mock_rag_service):
        """Test the chat endpoint with selected text (targeted RAG)"""
        # Mock the RAG service response
        mock_response = {
            "response": "Response based on selected text",
            "sources": [
                {
                    "chunk_id": "selected_text_test",
                    "content": "Selected text content",
                    "source_file": "selected_text",
                    "relevance_score": 1.0
                }
            ]
        }
        mock_rag_service.get_answer.return_value = mock_response
        
        # Prepare the request payload with selected_text
        payload = {
            "query": "Explain this?",
            "selected_text": "This is the text I selected",
            "book_id": "test-book-id"
        }
        
        # Make the request
        response = client.post("/api/v1/chat", json=payload)
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Response based on selected text"
        assert len(data["sources"]) == 1
        assert data["sources"][0]["source_file"] == "selected_text"
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to the RAG-Based AI Book Chatbot API"
    
    @patch('backend.routers.chat.IngestionPipeline')
    def test_ingest_endpoint(self, mock_ingestion_pipeline):
        """Test the ingest endpoint"""
        # Mock the ingestion pipeline
        mock_pipeline_instance = MagicMock()
        mock_pipeline_instance.process_and_store.return_value = 5
        mock_ingestion_pipeline.return_value = mock_pipeline_instance
        
        # Prepare the request payload
        payload = {
            "book_id": "test-book-id",
            "source_path": "./test-docs/"
        }
        
        # Make the request
        response = client.post("/api/v1/ingest", json=payload)
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["chunks_processed"] == 5
        assert data["book_id"] == "test-book-id"
    
    @patch('backend.routers.chat.SessionService')
    @patch('backend.database.SessionLocal')
    def test_session_history_endpoint(self, mock_session_local, mock_session_service_class):
        """Test the session history endpoint"""
        # Mock the session service
        mock_session_service = MagicMock()
        mock_session_service.get_session_history.return_value = [
            {
                "message_id": "test-message-id",
                "role": "user",
                "content": "Test message",
                "sources": []
            }
        ]
        mock_session_service_class.return_value = mock_session_service
        
        # Mock the database session
        mock_db_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_db_session
        
        # Make the request with a valid session ID
        session_id = "550e8400-e29b-41d4-a716-446655440000"
        response = client.get(f"/api/v1/sessions/{session_id}")
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == session_id
        assert len(data["messages"]) == 1
        assert data["messages"][0]["content"] == "Test message"
    
    def test_session_history_endpoint_invalid_id(self):
        """Test the session history endpoint with invalid session ID"""
        # Make the request with an invalid session ID
        response = client.get("/api/v1/sessions/invalid-id")
        
        # Verify the response
        assert response.status_code == 400
        data = response.json()
        assert "Invalid session_id format" in data["detail"]