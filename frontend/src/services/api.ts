import { ChatRequest, ChatResponse, IngestionRequest, IngestionResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

class ApiService {
  async chat(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: request.user_query,
          session_id: request.session_id,
          selected_text: request.selected_text
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      return {
        response: data.answer,
        citations: data.sources.map((source: any) => ({
          chunk_id: source.id || '',
          text: source.content || source.text || '',
          confidence: source.score || 0.8,
          metadata: source.metadata || {}
        })),
        session_id: data.session_id
      };
    } catch (error) {
      console.error('Error in chat API call:', error);
      throw error;
    }
  }

  async ingestBook(request: IngestionRequest): Promise<IngestionResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/ingest`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error in ingest API call:', error);
      throw error;
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}

export const apiService = new ApiService();