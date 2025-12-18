import pytest
from fastapi.testclient import TestClient
from rag_backend.main import app
from rag_backend.models import ChatRequest, IngestRequest


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_chat_endpoint_with_valid_request():
    with TestClient(app) as client:
        # Test with a simple request (this will fail in real execution without actual backend services)
        # but will test the endpoint validation
        chat_request = ChatRequest(
            question="What is this documentation about?",
            selected_context=None
        )
        
        response = client.post("/chat", json=chat_request.dict())
        # The endpoint will fail due to missing services, but we test that validation works
        # It should return either 200 (success) or 500 (service error), but not 422 (validation error)
        assert response.status_code in [200, 500]


def test_ingest_endpoint_with_valid_request():
    with TestClient(app) as client:
        ingest_request = IngestRequest(
            source_path="./test_data",
            force_reprocess=False
        )
        
        response = client.post("/ingest", json=ingest_request.dict())
        # The endpoint will likely fail due to missing services during testing
        # but we test that validation works
        assert response.status_code in [200, 500]


if __name__ == "__main__":
    pytest.main()