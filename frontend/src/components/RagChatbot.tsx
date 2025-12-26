import React, { useState, useEffect } from 'react';
import { ChatWindow } from './ChatWindow';
import { TextSelectionHandler } from './TextSelectionHandler';
import { useTextSelection } from '../hooks/useTextSelection';
import { apiClient } from '../services/apiClient';
import { ChatMessage, ChatRequest } from '../types';

interface RagChatbotProps {
  bookId: string;
  userId?: string;
  sessionId?: string;
  onSessionChange?: (sessionId: string) => void;
}

export const RagChatbot: React.FC<RagChatbotProps> = ({
  bookId,
  userId = 'default-user',
  sessionId: propSessionId,
  onSessionChange
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState<string | undefined>(propSessionId);
  const { selectedText, clearSelection } = useTextSelection();

  // Initialize with any existing session
  useEffect(() => {
    if (propSessionId) {
      setCurrentSessionId(propSessionId);
    }
  }, [propSessionId]);

  const handleSend = async (query: string) => {
    // Add user message to UI immediately
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: query,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const request: ChatRequest = {
        user_query: query,
        book_id: bookId,
        selected_text: selectedText || undefined,
        session_id: currentSessionId,
      };

      const response = await apiClient.chat(request);

      // Update session ID if it was created
      if (response.session_id && !currentSessionId) {
        setCurrentSessionId(response.session_id);
        onSessionChange?.(response.session_id);
      }

      // Add assistant response to UI
      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        content: response.response,
        role: 'assistant',
        timestamp: new Date(),
        citations: response.citations,
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Clear the selected text after using it
      if (selectedText) {
        clearSelection();
      }
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        content: 'Sorry, I encountered an error processing your request.',
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="rag-chatbot">
      <TextSelectionHandler />
      <ChatWindow 
        messages={messages} 
        onSend={handleSend} 
        isLoading={isLoading}
        selectedText={selectedText}
      />
    </div>
  );
};