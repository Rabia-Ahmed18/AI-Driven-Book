# API Contracts: AI/Spec-Driven Book Creation

## Overview

This document describes the API contracts for the AI/Spec-Driven Book Creation project. These APIs facilitate the creation, management, and deployment of the technical book.

## Book Management API

### Create New Book
- **Endpoint**: POST `/api/books`
- **Description**: Creates a new technical book project
- **Request Body**:
  ```
  {
    "title": "string (required)",
    "description": "string (required)",
    "authors": "array<string> (required)",
    "specId": "string (reference to spec)"
  }
  ```
- **Response**:
  - 201 Created: `{ id: string, title: string, createdAt: Date, status: 'draft' }`
  - 400 Bad Request: Validation errors
- **Authentication**: Required

### Get Book Details
- **Endpoint**: GET `/api/books/{id}`
- **Description**: Retrieves detailed information about a book
- **Parameters**: 
  - id: string (path parameter, required)
- **Response**:
  - 200 OK: `{ id: string, title: string, description: string, authors: array<string>, chapters: array<Chapter>, status: string, createdAt: Date, updatedAt: Date }`
  - 404 Not Found: If book doesn't exist
- **Authentication**: Required

### Update Book
- **Endpoint**: PUT `/api/books/{id}`
- **Description**: Updates book information
- **Parameters**: 
  - id: string (path parameter, required)
- **Request Body**:
  ```
  {
    "title": "string (optional)",
    "description": "string (optional)",
    "authors": "array<string> (optional)"
  }
  ```
- **Response**:
  - 200 OK: `{ id: string, title: string, updatedAt: Date }`
  - 400 Bad Request: Validation errors
  - 404 Not Found: If book doesn't exist
- **Authentication**: Required

## Chapter Management API

### Create Chapter
- **Endpoint**: POST `/api/books/{bookId}/chapters`
- **Description**: Creates a new chapter in a book
- **Parameters**:
  - bookId: string (path parameter, required)
- **Request Body**:
  ```
  {
    "title": "string (required)",
    "position": "number (required)",
    "status": "'draft' | 'review' | 'approved' | 'published'"
  }
  ```
- **Response**:
  - 201 Created: `{ id: string, title: string, position: number, status: string, createdAt: Date }`
  - 400 Bad Request: Validation errors
  - 404 Not Found: If book doesn't exist
- **Authentication**: Required

### Update Chapter Content
- **Endpoint**: PUT `/api/books/{bookId}/chapters/{chapterId}/content`
- **Description**: Updates the content of a chapter
- **Parameters**:
  - bookId: string (path parameter, required)
  - chapterId: string (path parameter, required)
- **Request Body**:
  ```
  {
    "content": "string (required)"
  }
  ```
- **Response**:
  - 200 OK: `{ id: string, content: string, updatedAt: Date }`
  - 400 Bad Request: Validation errors
  - 404 Not Found: If book or chapter doesn't exist
- **Authentication**: Required

### Publish Chapter
- **Endpoint**: POST `/api/books/{bookId}/chapters/{chapterId}/publish`
- **Description**: Publishes a chapter (makes it live)
- **Parameters**:
  - bookId: string (path parameter, required)
  - chapterId: string (path parameter, required)
- **Response**:
  - 200 OK: `{ id: string, status: 'published', updatedAt: Date }`
  - 404 Not Found: If book or chapter doesn't exist
  - 409 Conflict: If chapter is not in approved state
- **Authentication**: Required

## Section Management API

### Create Section
- **Endpoint**: POST `/api/books/{bookId}/chapters/{chapterId}/sections`
- **Description**: Creates a new section within a chapter
- **Parameters**:
  - bookId: string (path parameter, required)
  - chapterId: string (path parameter, required)
- **Request Body**:
  ```
  {
    "title": "string (required)",
    "position": "number (required)",
    "content": "string (required)"
  }
  ```
- **Response**:
  - 201 Created: `{ id: string, title: string, position: number, createdAt: Date }`
  - 400 Bad Request: Validation errors
  - 404 Not Found: If book or chapter doesn't exist
- **Authentication**: Required

## Specification API

### Create Specification
- **Endpoint**: POST `/api/specifications`
- **Description**: Creates a new specification document
- **Request Body**:
  ```
  {
    "title": "string (required)",
    "content": "string (required)",
    "specId": "string (globally unique)"
  }
  ```
- **Response**:
  - 201 Created: `{ id: string, title: string, specId: string, createdAt: Date, status: 'draft' }`
  - 400 Bad Request: Validation errors (e.g., duplicate specId)
- **Authentication**: Required

### Approve Specification
- **Endpoint**: POST `/api/specifications/{id}/approve`
- **Description**: Approves a specification for implementation
- **Parameters**:
  - id: string (path parameter, required)
- **Response**:
  - 200 OK: `{ id: string, status: 'approved', updatedAt: Date }`
  - 404 Not Found: If specification doesn't exist
  - 409 Conflict: If specification is not in draft or review state
- **Authentication**: Required

## Build and Deployment API

### Trigger Build
- **Endpoint**: POST `/api/books/{id}/build`
- **Description**: Triggers a build of the entire book
- **Parameters**:
  - id: string (path parameter, required)
- **Response**:
  - 202 Accepted: `{ buildId: string, status: 'in-progress', queuedAt: Date }`
  - 404 Not Found: If book doesn't exist
- **Authentication**: Required

### Get Build Status
- **Endpoint**: GET `/api/builds/{buildId}`
- **Description**: Retrieves the status of a specific build
- **Parameters**:
  - buildId: string (path parameter, required)
- **Response**:
  - 200 OK: `{ id: string, status: 'success' | 'failed' | 'in-progress', startedAt: Date, completedAt: Date, logs: array<string> }`
  - 404 Not Found: If build doesn't exist
- **Authentication**: Required

### Deploy Book
- **Endpoint**: POST `/api/books/{id}/deploy`
- **Description**: Deploys the built book to the target platform
- **Parameters**:
  - id: string (path parameter, required)
- **Response**:
  - 202 Accepted: `{ deploymentId: string, status: 'in-progress', queuedAt: Date }`
  - 404 Not Found: If book doesn't exist
- **Authentication**: Required

## Error Response Format

All error responses follow this format:
```
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object (optional additional details)"
  }
}
```

Common error codes:
- INVALID_REQUEST: Request parameters or body don't meet validation requirements
- RESOURCE_NOT_FOUND: Requested resource doesn't exist
- CONFLICT: Request conflicts with current state (e.g., publishing non-approved chapter)
- UNAUTHORIZED: Authentication required or invalid credentials
- INTERNAL_ERROR: Unexpected server error