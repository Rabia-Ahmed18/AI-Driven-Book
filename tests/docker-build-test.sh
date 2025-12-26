#!/bin/bash
# Test script to verify Docker image builds successfully

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Docker build test..."

# Build the Docker image
docker build -t test-book-assistant-backend . --no-cache

# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "✅ Docker build test PASSED"
    echo "Docker image built successfully"
    
    # Get image size
    IMAGE_SIZE=$(docker inspect test-book-assistant-backend | grep -o '"Size": [0-9]*' | cut -d' ' -f2)
    IMAGE_SIZE_MB=$((IMAGE_SIZE / 1024 / 1024))
    
    echo "Docker image size: $IMAGE_SIZE_MB MB"
    
    # Check if image size is under 2GB (2048 MB)
    if [ $IMAGE_SIZE_MB -lt 2048 ]; then
        echo "✅ Image size constraint PASSED (< 2GB)"
    else
        echo "❌ Image size constraint FAILED (>= 2GB)"
        exit 1
    fi
    
    # Clean up - remove the test image
    docker rmi test-book-assistant-backend
    
    echo "✅ All Docker tests PASSED"
    exit 0
else
    echo "❌ Docker build test FAILED"
    exit 1
fi