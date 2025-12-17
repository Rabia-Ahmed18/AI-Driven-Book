---
sidebar_position: 1
---

# RAG Chatbot Integration

The RAG (Retrieval-Augmented Generation) Chatbot provides an AI-powered interface for users to ask questions about the book content. It leverages a vector database to retrieve relevant information and generates responses based on the book's content.

## Features

- **Context-Aware Q&A**: Ask questions about the entire book or specific selected text
- **Source Citations**: All answers include references to the original content
- **Text Selection**: Highlight text and ask questions about it directly
- **Real-time Responses**: Fast, relevant answers powered by OpenAI

## How to Use

1. Type your question in the input field at the bottom of the chat interface
2. If you have text selected on the page, a special "Ask about selection" button will appear
3. Responses will include citations to the source documents

## Technical Implementation

The RAG Chatbot is implemented as a React component that communicates with our FastAPI backend. The backend processes queries using:

- **Qdrant** for vector similarity search
- **Neon Postgres** for metadata storage
- **OpenAI** for language model responses
- **Recursive text splitting** for document chunking

## Integration with Docusaurus

The chatbot component (RAGChatbot.tsx) is designed to be easily integrated into the Docusaurus layout. It can be added as:

- A sidebar widget
- A footer button that expands into a chat interface
- A dedicated page
- An overlay that appears on demand

For best user experience, we recommend integrating it as a persistent sidebar or a floating action button.