// API service for chat interactions
class ChatApiService {
  constructor() {
    this.baseURL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';
  }

  // Method to send a chat message
  async sendMessage(question, sessionId = null, selectedText = null) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          session_id: sessionId,
          selected_text: selectedText
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  // Method to send a query
  async sendQuery(question, sessionId = null, selectedText = null) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          session_id: sessionId,
          selected_text: selectedText
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending query:', error);
      throw error;
    }
  }

  // Method to get chat history (if needed)
  async getChatHistory(sessionId) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/chat/history/${sessionId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting chat history:', error);
      throw error;
    }
  }
}

// Export a singleton instance
export const chatApiService = new ChatApiService();

export default chatApiService;