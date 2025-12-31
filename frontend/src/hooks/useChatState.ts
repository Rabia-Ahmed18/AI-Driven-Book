import { useState, useEffect } from 'react';
import { ChatMessage } from '../types';

export interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  sessionId: string | null;
  error: string | null;
}

export interface ChatActions {
  addMessage: (message: ChatMessage) => void;
  clearMessages: () => void;
  setIsLoading: (loading: boolean) => void;
  setSessionId: (id: string | null) => void;
  setError: (error: string | null) => void;
}

export const useChatState = (initialMessages: ChatMessage[] = []): [ChatState, ChatActions] => {
  const [state, setState] = useState<ChatState>({
    messages: initialMessages,
    isLoading: false,
    sessionId: null,
    error: null,
  });

  const actions: ChatActions = {
    addMessage: (message: ChatMessage) => {
      setState(prev => ({
        ...prev,
        messages: [...prev.messages, message]
      }));
    },
    clearMessages: () => {
      setState(prev => ({
        ...prev,
        messages: []
      }));
    },
    setIsLoading: (loading: boolean) => {
      setState(prev => ({
        ...prev,
        isLoading: loading
      }));
    },
    setSessionId: (id: string | null) => {
      setState(prev => ({
        ...prev,
        sessionId: id
      }));
    },
    setError: (error: string | null) => {
      setState(prev => ({
        ...prev,
        error: error
      }));
    }
  };

  return [state, actions];
};