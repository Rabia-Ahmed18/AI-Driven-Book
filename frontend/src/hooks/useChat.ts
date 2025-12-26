import { useState } from 'react';
import { ChatMessage } from '../types';

export const useChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (content: string, context?: string) => {
    setIsLoading(true);
    
    try {
      // In a real implementation, this would call the API
      // For now, we'll just simulate an API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Add the user's message
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        content,
        role: 'user',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, userMessage]);
      
      // Simulate a response
      const responseMessage: ChatMessage = {
        id: `response-${Date.now()}`,
        content: `This is a simulated response to: "${content}". In a real implementation, this would come from the backend API.`,
        role: 'assistant',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, responseMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    messages,
    isLoading,
    sendMessage,
    setMessages
  };
};