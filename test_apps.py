#!/usr/bin/env python3
"""
Test script to verify that both backend applications can be loaded properly.
"""
import os
import sys

# Set minimal required environment variables for the test
os.environ.setdefault('OPENAI_API_KEY', 'test-key')
os.environ.setdefault('QDRANT_URL', 'http://localhost:6333')
os.environ.setdefault('QDRANT_API_KEY', 'test-key')
os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('NEON_DATABASE_URL', 'postgresql://test:test@localhost/test')

def test_backend_app():
    """Test loading the backend/src/main.py app"""
    try:
        from backend.src.main import app
        print("SUCCESS: Backend app loaded successfully")
        return True
    except Exception as e:
        print(f"ERROR: Backend app failed to load: {e}")
        return False

def test_app_app():
    """Test loading the app/main.py app"""
    try:
        from app.main import app
        print("SUCCESS: App app loaded successfully")
        return True
    except Exception as e:
        print(f"ERROR: App app failed to load: {e}")
        return False

if __name__ == "__main__":
    print("Testing application loading...")

    backend_ok = test_backend_app()
    app_ok = test_app_app()

    if backend_ok and app_ok:
        print("\nSUCCESS: All applications loaded successfully!")
        sys.exit(0)
    else:
        print("\nERROR: Some applications failed to load!")
        sys.exit(1)