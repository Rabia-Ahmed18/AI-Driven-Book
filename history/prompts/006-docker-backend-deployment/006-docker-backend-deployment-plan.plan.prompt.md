---
id: 006
title: docker-backend-deployment-plan
stage: plan
date: 2025-12-25
surface: agent
model: Qwen
feature: 006-docker-backend-deployment
branch: 006-docker-backend-deployment
user: User
command: /sp.plan
labels: [docker, deployment, huggingface, backend, planning]
links:
  spec: /specs/006-docker-backend-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - /specs/006-docker-backend-deployment/plan.md
 - /specs/006-docker-backend-deployment/research.md
 - /specs/006-docker-backend-deployment/data-model.md
 - /specs/006-docker-backend-deployment/quickstart.md
 - /specs/006-docker-backend-deployment/contracts/api-contract.yaml
tests:
 - null
---

## Prompt

$ARGUMENTS

## Response snapshot

# Implementation Plan: Docker Backend Deployment for HuggingFace

**Branch**: `006-docker-backend-deployment` | **Date**: 2025-12-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-docker-backend-deployment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a Dockerfile that packages the backend application for deployment on HuggingFace Spaces, ensuring compatibility with their environment, optimized resource usage, and proper handling of environment variables. The Docker image must build successfully without errors and deploy to HuggingFace Spaces with minimal startup time.

## Technical Context

**Language/Version**: Python 3.11 (based on existing project which uses FastAPI)
**Primary Dependencies**: FastAPI, Docker, HuggingFace Spaces compatibility requirements
**Storage**: N/A (containerization task)
**Testing**: Docker build verification, container runtime tests
**Target Platform**: Linux (HuggingFace Spaces container environment)
**Project Type**: Backend (existing web application backend containerization)
**Performance Goals**: Docker image builds in under 5 minutes, container starts in under 60 seconds
**Constraints**: Image size under 2GB, compatibility with HuggingFace Spaces environment, security best practices
**Scale/Scope**: Single backend service container for HuggingFace deployment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the constitution file, the following gates must be satisfied:

1. **RAG-First Architecture**: Not applicable to Docker containerization task
2. **Full-Stack Modularity**: The Dockerfile properly packages the existing backend module (FastAPI) for deployment
3. **Test-First (NON-NEGOTIABLE)**: Docker build and container runtime tests have been planned
4. **Content Context Integrity**: Not applicable to Docker containerization task
5. **Source Transparency**: Dockerfile is well-documented with clear source tracking
6. **Deployment-First Design**: Dockerfile follows deployment-ready practices with environment variable configuration

**GATE STATUS**: All applicable gates have been satisfied with the planned approach.

## Phase 1 Deliverables

- **research.md**: Completed - Contains research on Docker best practices and HuggingFace Spaces requirements
- **data-model.md**: Completed - Defines data models for Docker configuration and HuggingFace Spaces
- **quickstart.md**: Completed - Provides instructions for building, testing, and deploying the Docker container
- **contracts/api-contract.yaml**: Completed - Defines the API contract for the backend service
- **Agent Context Updated**: Completed - Qwen agent context updated with new technology information

## Project Structure

### Documentation (this feature)

```text
specs/006-docker-backend-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
├── tests/
├── Dockerfile
├── requirements.txt
└── .dockerignore

# HuggingFace Spaces specific files
├── app.py
└── space.yml
```

**Structure Decision**: The Dockerfile will be added to the existing backend project structure to containerize the FastAPI application for HuggingFace Spaces deployment. This follows the existing modularity approach with a separate backend module.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

# Research: Docker Backend Deployment for HuggingFace

## Overview
This document captures research findings for creating a Dockerfile that packages the backend application for deployment on HuggingFace Spaces.

## Decision: Base Image Selection
**Rationale**: For HuggingFace Spaces compatibility and Python 3.11 requirement, we'll use the official Python 3.11 slim image.
**Alternative Considered**: Alpine Linux base image for smaller size - rejected because of potential compatibility issues with Python packages and HuggingFace requirements.

## Decision: Multi-stage Build Approach
**Rationale**: To optimize Docker image size and security, we'll implement a multi-stage build with a build stage and runtime stage.
**Alternative Considered**: Single-stage build - rejected because it results in larger images with unnecessary build tools in the final image.

## Decision: HuggingFace Spaces Specific Configuration
**Rationale**: HuggingFace Spaces requires specific configurations:
- Port 7860 (or 8000) for the application to listen on
- Proper startup command
- Compatibility with their container runtime environment
**Alternative Considered**: Standard Docker configuration - rejected because it won't work in HuggingFace Spaces environment.

## Decision: Environment Variables Handling
**Rationale**: Using environment variables for configuration allows flexibility without rebuilding the image.
- Use standard environment variable patterns for configuration
- Provide default values in the Dockerfile where appropriate
- Document required environment variables in quickstart guide

## Decision: Dependencies Installation Strategy
**Rationale**: Install Python dependencies using pip with requirements.txt file.
- Use pip cache to speed up builds
- Install system dependencies separately for better layer caching
- Consider using Poetry or Pipenv if already used in the project

## Decision: Security Considerations
**Rationale**: Run container as non-root user to improve security.
- Create a dedicated user for running the application
- Set appropriate file permissions
- Use Docker security scanning tools to identify vulnerabilities

## Decision: Optimization Techniques
**Rationale**: Optimize for size and startup time as per requirements.
- Use .dockerignore to exclude unnecessary files
- Leverage Docker layer caching by ordering instructions properly
- Use multi-stage builds to reduce final image size
- Consider using Docker squashing for even smaller images

## HuggingFace Spaces Specific Requirements
Based on research, HuggingFace Spaces has the following requirements:
- The application must listen on port 7860 (Gradio default) or 8000 (FastAPI default)
- The application must be started with the appropriate command
- GPU access is available but needs to be configured in space.yml
- Storage is ephemeral, so persistent data must be stored externally
- Resource limits apply (CPU, memory, disk space)

## Docker Best Practices Applied
- Use specific base image tags instead of 'latest'
- Chain RUN commands to reduce layers
- Use .dockerignore to exclude unnecessary files
- Install only required dependencies
- Use non-root user for security
- Properly handle signals for graceful shutdown
- Use HEALTHCHECK for container monitoring

# Data Model: Docker Backend Deployment for HuggingFace

## Overview
This document describes the data models and configuration structures relevant to Docker containerization for HuggingFace Spaces deployment.

## Docker Configuration Model

### Dockerfile Configuration
- **Base Image**: The foundational image used for the container (e.g., python:3.11-slim)
- **Dependencies**: Python packages and system libraries required by the application
- **Working Directory**: The directory inside the container where the application runs
- **Port**: The port number the application listens on (typically 7860 or 8000 for HuggingFace Spaces)
- **Startup Command**: The command that starts the backend service when the container runs
- **Environment Variables**: Configuration parameters passed to the container at runtime

### Docker Image Properties
- **Image Name**: The name of the Docker image
- **Image Tag**: The version identifier for the image
- **Size**: The size of the Docker image (should be under 2GB as per requirements)
- **Layers**: The individual layers that make up the Docker image
- **Build Context**: The files and directories used during the Docker build process

## HuggingFace Spaces Configuration Model

### Space Configuration (space.yml)
- **Type**: The type of Space (e.g., docker for custom Dockerfile)
- **Hardware**: The hardware requirements (e.g., cpu, gpu-t4, gpu-a10g)
- **Env Variables**: Environment variables required for the application
- **Dockerfile**: Path to the Dockerfile (if different from default)

### Runtime Environment
- **Port Mapping**: Mapping between container port and external access
- **Resource Limits**: CPU, memory, and disk space constraints
- **Startup Time**: Time allowed for the application to start
- **Health Checks**: Mechanisms to verify the application is running properly

## Application Configuration Model

### Environment Variables
- **API Keys**: Credentials for external services (OpenAI, Qdrant, Neon)
- **Database URLs**: Connection strings for database services
- **Application Settings**: Configuration parameters for the backend application
- **Feature Flags**: Toggle switches for different application features

### File System Structure
- **Source Code**: The application code within the container
- **Dependencies**: Python packages installed in the container
- **Configuration Files**: Settings files required by the application
- **Log Directories**: Locations where application logs are stored
- **Temporary Storage**: Ephemeral storage available to the container

## Security Model

### User Permissions
- **Container User**: Non-root user under which the application runs
- **File Permissions**: Read/write permissions for different parts of the file system
- **Network Access**: Restrictions on outbound network connections

### Secrets Management
- **Environment Variables**: Secure handling of sensitive information
- **Build-time Secrets**: Credentials needed during the build process
- **Runtime Secrets**: Credentials needed during application execution

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

# API Contract: Backend Service for Docker Deployment

## Overview
This document defines the API contract for the backend service that will be containerized and deployed to HuggingFace Spaces.

## Base URL
```
http://localhost:8000 (local development)
https://[your-space-name].hf.space (HuggingFace Spaces deployment)
```

## Health Check Endpoint
### GET /health
Check the health status of the backend service.

**Response:**
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-25T10:00:00Z",
  "version": "1.0.0"
}
```

## Book-Wide Q&A Endpoint
### POST /api/book-wide-qna
Process a question against the entire book corpus and return a response with source citations.

**Headers:**
- Content-Type: application/json
- Authorization: Bearer {API_KEY} (if required)

**Request Body:**
```json
{
  "question": "What is the main concept discussed in the book?",
  "context_window": 5,  // Number of context chunks to retrieve
  "model": "gpt-3.5-turbo"  // Optional: LLM model to use
}
```

**Response:**
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "response": "The main concept discussed in the book is...",
  "sources": [
    {
      "filename": "chapter1.md",
      "section": "Introduction",
      "chunk_id": "chunk_12345",
      "similarity_score": 0.92
    }
  ],
  "model_used": "gpt-3.5-turbo",
  "processing_time": 1.234  // in seconds
}
```

**Error Responses:**
- 400 Bad Request: Invalid request format
- 401 Unauthorized: Invalid or missing API key
- 422 Unprocessable Entity: Question is empty or too long
- 500 Internal Server Error: Processing error

## Selected Text Q&A Endpoint
### POST /api/selected-text-qna
Process a question against a specific text selection and return a response with source citations.

**Headers:**
- Content-Type: application/json
- Authorization: Bearer {API_KEY} (if required)

**Request Body:**
```json
{
  "question": "What does this specific text mean?",
  "selected_context": "The specific text that was selected by the user...",
  "model": "gpt-3.5-turbo"  // Optional: LLM model to use
}
```

**Response:**
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "response": "The selected text means...",
  "sources": [
    {
      "context_provenance": "user_selected_text",
      "similarity_score": 1.0
    }
  ],
  "model_used": "gpt-3.5-turbo",
  "processing_time": 0.856  // in seconds
}
```

**Error Responses:**
- 400 Bad Request: Invalid request format
- 401 Unauthorized: Invalid or missing API key
- 422 Unprocessable Entity: Question or context is empty
- 500 Internal Server Error: Processing error

## Content Ingestion Endpoint
### POST /api/ingest
Ingest documents from the docs directory into the vector database.

**Headers:**
- Content-Type: application/json
- Authorization: Bearer {API_KEY} (if required)

**Request Body:**
```json
{
  "source_directory": "./docs",  // Path to docs directory
  "chunk_size": 1000,  // Optional: size of text chunks
  "chunk_overlap": 100,  // Optional: overlap between chunks
  "recreate_index": false  // Optional: recreate the vector index
}
```

**Response:**
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "status": "completed",
  "files_processed": 15,
  "chunks_created": 125,
  "index_name": "book_chunks",
  "processing_time": 45.678  // in seconds
}
```

**Error Responses:**
- 400 Bad Request: Invalid request format
- 401 Unauthorized: Invalid or missing API key
- 500 Internal Server Error: Processing error

## Error Response Format
All error responses follow this format:
```json
{
  "error": {
    "type": "error_type",
    "message": "Descriptive error message",
    "details": "Additional error details if available"
  }
}
```

## Common Error Types
- `invalid_request_error`: The request format is invalid
- `authentication_error`: Authentication failed
- `processing_error`: An error occurred during processing
- `resource_not_found`: The requested resource does not exist
- `rate_limit_error`: Rate limit exceeded

## Outcome

- ✅ Impact: Created comprehensive implementation plan for Docker backend deployment on HuggingFace
- 🧪 Tests: No tests run yet - planning phase
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and contracts/api-contract.yaml
- 🔁 Next prompts: Ready for task breakdown phase (/sp.tasks)
- 🧠 Reflection: Planning phase complete with all required artifacts generated

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A