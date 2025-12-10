# Data Model: AI/Spec-Driven Book Creation

Updated: December 9, 2025

## Overview

This document describes the data model for the AI/Spec-Driven Book Creation project. It defines the entities, their attributes, relationships, and validation rules that support the creation and management of the technical book.

## Key Entities

### Book
- **Description**: The main entity representing the complete technical book
- **Attributes**:
  - id: string (unique identifier)
  - title: string (title of the book)
  - description: string (brief description)
  - version: string (version of the book)
  - authors: array<string> (list of authors/writers)
  - createdAt: Date (when the book was created)
  - updatedAt: Date (last update timestamp)
  - published: boolean (whether the book is published)
- **Relationships**:
  - Has many: Chapter
  - Belongs to: Specification
- **Validation rules**:
  - title must be 1-100 characters
  - description must be 1-500 characters
  - authors must contain at least one author
  - version must follow semantic versioning

### Chapter
- **Description**: A major section of the book that corresponds to a specific topic or theme
- **Attributes**:
  - id: string (unique identifier)
  - title: string (title of the chapter)
  - content: string (the actual MDX content of the chapter)
  - position: number (order in the book, 1-indexed)
  - wordCount: number (estimated word count)
  - status: enum (draft, review, approved, published)
  - createdAt: Date (when the chapter was created)
  - updatedAt: Date (last update timestamp)
  - published: boolean (whether the chapter is published)
- **Relationships**:
  - Belongs to: Book
  - Has many: Section
  - Belongs to: Specification
- **Validation rules**:
  - title must be 1-100 characters
  - position must be a positive integer
  - status must be one of the allowed values
  - content cannot exceed 50,000 characters

### Section
- **Description**: A subsection within a chapter that addresses specific aspects of the topic
- **Attributes**:
  - id: string (unique identifier)
  - title: string (title of the section)
  - content: string (the actual content of the section)
  - position: number (order within the chapter, 1-indexed)
  - wordCount: number (estimated word count)
  - status: enum (draft, review, approved, published)
  - createdAt: Date (when the section was created)
  - updatedAt: Date (last update timestamp)
- **Relationships**:
  - Belongs to: Chapter
  - Has many: CodeExample, Image
- **Validation rules**:
  - title must be 1-100 characters
  - position must be a positive integer
  - status must be one of the allowed values

### Specification
- **Description**: The formal requirement document that defines each chapter/section content and requirements
- **Attributes**:
  - id: string (unique identifier)
  - title: string (title of the specification)
  - content: string (the actual specification content)
  - version: string (version of the specification)
  - status: enum (draft, review, approved, archived)
  - createdAt: Date (when the spec was created)
  - updatedAt: Date (last update timestamp)
  - specId: string (unique ID for the spec referenced in MDX frontmatter)
- **Relationships**:
  - Has many: Book, Chapter, Section
  - Has many: ImplementationPlan
- **Validation rules**:
  - title must be 1-100 characters
  - content must not be empty
  - specId must be globally unique
  - status must be one of the allowed values

### ImplementationPlan
- **Description**: The technical implementation approach for creating the book content based on specifications
- **Attributes**:
  - id: string (unique identifier)
  - title: string (title of the plan)
  - content: string (the actual plan content)
  - version: string (version of the plan)
  - status: enum (draft, review, approved, completed)
  - createdAt: Date (when the plan was created)
  - updatedAt: Date (last update timestamp)
  - associatedSpecId: string (reference to the related specification)
- **Relationships**:
  - Belongs to: Specification
- **Validation rules**:
  - title must be 1-100 characters
  - content must not be empty
  - associatedSpecId must reference an existing specification

### CodeExample
- **Description**: Code samples included within sections that demonstrate concepts
- **Attributes**:
  - id: string (unique identifier)
  - title: string (brief title/description)
  - language: string (programming language for syntax highlighting)
  - code: string (the actual code content)
  - description: string (explanation of the code)
  - createdAt: Date (when the example was created)
  - updatedAt: Date (last update timestamp)
- **Relationships**:
  - Belongs to: Section
- **Validation rules**:
  - title must be 1-100 characters
  - language must be a valid syntax highlighting language
  - code must not be empty

### Image
- **Description**: Images included within sections that support the written content
- **Attributes**:
  - id: string (unique identifier)
  - altText: string (alt text for accessibility)
  - fileName: string (name of the image file)
  - caption: string (optional image caption)
  - width: number (optional display width)
  - height: number (optional display height)
  - createdAt: Date (when the image was added)
  - updatedAt: Date (last update timestamp)
- **Relationships**:
  - Belongs to: Section
- **Validation rules**:
  - altText must be 1-200 characters
  - fileName must have a valid image extension (.png, .jpg, .jpeg, .gif, .svg, .webp)
  - width and height must be positive numbers if provided

### DocusaurusSite
- **Description**: The generated static site with responsive design, i18n, and theme capabilities
- **Attributes**:
  - id: string (unique identifier)
  - config: object (site configuration)
  - navigation: object (sidebar and navbar configuration)
  - theme: object (theme customization)
  - deploymentUrl: string (URL of the deployed site)
  - isDeployed: boolean (whether the site is currently deployed)
  - lastDeployedAt: Date (timestamp of last deployment)
  - buildStatus: enum (success, failed, in-progress)
- **Relationships**:
  - Contains: Book
- **Validation rules**:
  - deploymentUrl must be a valid URL
  - buildStatus must be one of the allowed values

## State Transitions

### Chapter States
- draft → review (when ready for review)
- review → draft (if changes requested)
- review → approved (if approved)
- approved → published (when ready to go live)
- published → approved (when unpublished)

### Specification States
- draft → review (when ready for review)
- review → draft (if changes requested)
- review → approved (if approved)
- approved → archived (when no longer applicable)

## Relationships Summary

- Book (1) → Chapter (Many)
- Chapter (1) → Section (Many)
- Section (1) → CodeExample (Many)
- Section (1) → Image (Many)
- Specification (1) → Book (1)
- Specification (1) → ImplementationPlan (1)
- ImplementationPlan (1) → Specification (1)