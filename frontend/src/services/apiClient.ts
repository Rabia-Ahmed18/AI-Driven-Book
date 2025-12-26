import axios, { AxiosInstance } from 'axios';
import { 
  ChatRequest, 
  ChatResponse, 
  IngestionRequest, 
  IngestionResponse,
  Book,
  ChatSession,
  CreateSessionRequest
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000, // 30 seconds timeout
    });

    // Add request interceptor to include auth headers if needed
    this.client.interceptors.request.use(
      (config) => {
        // If we have an auth token, include it
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error);
        return Promise.reject(error);
      }
    );
  }

  // Chat API methods
  async chat(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await this.client.post<ChatResponse>('/api/v1/chat', {
        user_query: request.user_query,
        book_id: request.book_id,
        selected_text: request.selected_text,
        session_id: request.session_id
      });
      return response.data;
    } catch (error) {
      console.error('Error in chat API:', error);
      throw error;
    }
  }

  // Ingestion API methods
  async ingestBook(request: IngestionRequest): Promise<IngestionResponse> {
    try {
      const response = await this.client.post<IngestionResponse>('/api/v1/ingest', {
        title: request.title,
        author: request.author,
        content: request.content,
        metadata: request.metadata
      });
      return response.data;
    } catch (error) {
      console.error('Error in ingest API:', error);
      throw error;
    }
  }

  // Book API methods
  async getBooks(): Promise<Book[]> {
    try {
      const response = await this.client.get<Book[]>('/api/v1/books');
      return response.data;
    } catch (error) {
      console.error('Error in getBooks API:', error);
      throw error;
    }
  }

  async getBook(bookId: string): Promise<Book> {
    try {
      const response = await this.client.get<Book>(`/api/v1/books/${bookId}`);
      return response.data;
    } catch (error) {
      console.error('Error in getBook API:', error);
      throw error;
    }
  }

  async createBook(title: string, author: string, isbn?: string, description?: string, language?: string): Promise<Book> {
    try {
      const response = await this.client.post<Book>('/api/v1/books', {
        title,
        author,
        isbn,
        description,
        language
      });
      return response.data;
    } catch (error) {
      console.error('Error in createBook API:', error);
      throw error;
    }
  }

  // Session API methods
  async createSession(request: CreateSessionRequest): Promise<ChatSession> {
    try {
      const response = await this.client.post<ChatSession>('/api/v1/sessions', {
        user_id: request.user_id,
        book_id: request.book_id,
        title: request.title
      });
      return response.data;
    } catch (error) {
      console.error('Error in createSession API:', error);
      throw error;
    }
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error in health check:', error);
      throw error;
    }
  }
}

export const apiClient = new ApiClient();