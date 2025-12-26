// Type definitions for the RAG Chatbot application

export interface Book {
  id: string;
  title: string;
  author: string;
  isbn?: string;
  description?: string;
  language: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  chunk_count: number;
}

export interface ChatSession {
  id: string;
  user_id: string;
  book_id: string;
  title: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  active: boolean;
}

export interface Citation {
  chunk_id: string;
  text: string;
  confidence: number; // 0.0 to 1.0
  metadata?: Record<string, any>;
}

export interface Interaction {
  id: string;
  session_id: string;
  user_query: string;
  assistant_response: string;
  selected_text?: string;
  citations?: Citation[];
  created_at: string; // ISO date string
  response_time_ms?: number;
}

export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  citations?: Citation[];
}

export interface IngestionRequest {
  title: string;
  author: string;
  content: string;
  metadata?: Record<string, any>;
}

export interface IngestionResponse {
  book_id: string;
  chunks_created: number;
  processing_time_ms?: number;
}

export interface ChatRequest {
  user_query: string;
  book_id: string;
  selected_text?: string;
  session_id?: string;
}

export interface ChatResponse {
  response: string;
  citations: Citation[];
  response_time_ms?: number;
  session_id?: string;
}

export interface CreateSessionRequest {
  user_id: string;
  book_id: string;
  title?: string;
}