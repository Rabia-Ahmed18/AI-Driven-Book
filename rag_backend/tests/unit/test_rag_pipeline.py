import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, MagicMock
from rag_backend.models import ChatRequest, ChatResponse, IngestRequest, IngestResponse
from rag_backend.rag_core.rag_pipeline import RAGPipeline
from rag_backend.config import settings


@pytest.fixture
def mock_openai_client():
    client = AsyncMock()
    client.chat.completions.create = AsyncMock()
    return client


@pytest.fixture
def mock_qdrant_client():
    client = AsyncMock()
    client.search = AsyncMock()
    return client


@pytest.fixture
def mock_postgres_client():
    client = AsyncMock()
    client.get_metadata = AsyncMock()
    return client


@pytest.fixture
def rag_pipeline(mock_openai_client, mock_qdrant_client, mock_postgres_client):
    # Mock config object
    config = Mock()
    config.embedding_model = "text-embedding-3-small"
    config.top_k_chunks = 5
    
    return RAGPipeline(
        openai_client=mock_openai_client,
        qdrant_client=mock_qdrant_client,
        postgres_client=mock_postgres_client,
        config=config
    )


@pytest.mark.asyncio
async def test_generate_response_with_selected_context(rag_pipeline, mock_openai_client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test answer"
    mock_openai_client.chat.completions.create.return_value = mock_response
    
    # Test the method
    result = await rag_pipeline.generate_response(
        question="Test question?",
        context="Test context.",
        selected_context="Selected context."
    )
    
    # Assertions
    assert result == "Test answer"
    mock_openai_client.chat.completions.create.assert_called_once()
    
    # Check that the call was made with the selected context
    call_args = mock_openai_client.chat.completions.create.call_args
    assert "Selected context." in call_args[1]["messages"][1]["content"]


@pytest.mark.asyncio
async def test_generate_response_without_selected_context(rag_pipeline, mock_openai_client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test answer"
    mock_openai_client.chat.completions.create.return_value = mock_response
    
    # Test the method
    result = await rag_pipeline.generate_response(
        question="Test question?",
        context="Test context.",
        selected_context=None
    )
    
    # Assertions
    assert result == "Test answer"
    mock_openai_client.chat.completions.create.assert_called_once()
    
    # Check that the call was made with the general context
    call_args = mock_openai_client.chat.completions.create.call_args
    assert "Test context." in call_args[1]["messages"][1]["content"]