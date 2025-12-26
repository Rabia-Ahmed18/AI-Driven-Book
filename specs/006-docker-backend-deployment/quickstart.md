# Quickstart: Docker Backend Deployment for HuggingFace

## Overview
This guide provides instructions for building, testing, and deploying the backend application using Docker for HuggingFace Spaces.

## Prerequisites
- Docker installed on your system
- Access to the backend application source code
- HuggingFace account (for deployment)
- Appropriate API keys and environment variables

## Building the Docker Image

1. Navigate to the project root directory:
   ```bash
   cd /path/to/your/project
   ```

2. Build the Docker image:
   ```bash
   docker build -t your-backend-app:latest .
   ```

3. Verify the image was built successfully:
   ```bash
   docker images | grep your-backend-app
   ```

## Testing the Docker Container Locally

1. Run the container locally:
   ```bash
   docker run -p 8000:8000 -e API_KEY=your_api_key -e DATABASE_URL=your_db_url your-backend-app:latest
   ```

2. Access the application at `http://localhost:8000`

3. Verify that the application functions as expected

## Deploying to HuggingFace Spaces

1. Create a new Space on HuggingFace or use an existing one

2. Add your repository to the Space:
   - If using Git, add the repository URL
   - If using Docker, ensure your Dockerfile is in the repository root

3. Configure environment variables in the Space settings:
   - API_KEY: Your OpenAI API key
   - DATABASE_URL: Connection string for your Neon database
   - QDRANT_URL: URL for your Qdrant vector database
   - QDRANT_API_KEY: API key for your Qdrant database

4. The Space will automatically build and deploy your application using the Dockerfile

## Environment Variables

Required environment variables for the application:

- `API_KEY`: OpenAI API key for LLM interactions
- `DATABASE_URL`: Connection string for Neon PostgreSQL database
- `QDRANT_URL`: URL for Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant database (if required)
- `DEBUG`: Set to 'True' for debug mode (optional)

## Dockerfile Structure

The Dockerfile follows these steps:
1. Uses Python 3.11 slim as base image
2. Sets up working directory
3. Copies and installs Python dependencies
4. Copies application code
5. Exposes port 8000
6. Defines startup command

## Troubleshooting

### Container won't start
- Check logs: `docker logs <container_id>`
- Verify environment variables are set correctly
- Ensure the exposed port matches the application's listening port

### Application crashes after startup
- Check if all required environment variables are provided
- Verify database and external service connections
- Review application logs for specific error messages

### Slow startup time
- Optimize dependencies in requirements.txt
- Use multi-stage builds to reduce image size
- Review startup scripts for performance issues

## Best Practices

- Keep Docker image size under 2GB
- Use non-root user for security
- Implement health checks for container monitoring
- Use .dockerignore to exclude unnecessary files
- Regularly update base images for security patches