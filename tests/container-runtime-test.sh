#!/bin/bash
# Test script to verify Docker container runs and exposes the correct port

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Docker container runtime test..."

# Build the Docker image
docker build -t test-book-assistant-backend . --no-cache

# Run the container in detached mode
docker run -d --name test-container -p 8001:8000 \
  -e OPENAI_API_KEY=test-key \
  -e QDRANT_URL=test-url \
  -e QDRANT_API_KEY=test-key \
  -e NEON_DATABASE_URL=test-db-url \
  test-book-assistant-backend

# Wait a few seconds for the container to start
sleep 10

# Check if the container is running
if [ "$(docker inspect -f '{{.State.Running}}' test-container)" = "true" ]; then
    echo "✅ Container is running"
    
    # Test if the health endpoint is accessible
    # We'll use curl to check the health endpoint, but if it's not available in the container, we'll just verify the port is open
    if nc -z localhost 8001; then
        echo "✅ Port 8000 is accessible on the container"
        echo "✅ Docker container runtime test PASSED"
        
        # Clean up
        docker stop test-container
        docker rm test-container
        docker rmi test-book-assistant-backend
        
        exit 0
    else
        echo "❌ Port 8000 is not accessible"
        # Print container logs for debugging
        echo "Container logs:"
        docker logs test-container
        
        # Clean up
        docker stop test-container
        docker rm test-container
        docker rmi test-book-assistant-backend
        
        exit 1
    fi
else
    echo "❌ Container is not running"
    # Print container logs for debugging
    echo "Container logs:"
    docker logs test-container
    
    # Clean up
    docker stop test-container
    docker rm test-container
    docker rmi test-book-assistant-backend
    
    exit 1
fi