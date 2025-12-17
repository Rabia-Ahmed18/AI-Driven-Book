import React, { useState, useEffect, useRef } from 'react';
import './RAGChatbot.css';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  citations?: string[];
}

interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error?: string;
  selectedText: string | null;
}

const RAGChatbot: React.FC = () => {
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    selectedText: null,
  });
  
  const [inputValue, setInputValue] = useState<string>('');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [chatState.messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Add event listener for text selection
  useEffect(() => {
    const handleSelectionChange = () => {
      const selectedText = window.getSelection()?.toString().trim();
      setChatState(prev => ({
        ...prev,
        selectedText: selectedText || null
      }));
    };

    document.addEventListener('selectionchange', handleSelectionChange);
    
    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputValue.trim() || chatState.isLoading) return;

    // Add user message to chat
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: undefined
    }));

    setInputValue('');

    try {
      // Call the backend API
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: inputValue,
          selected_context: chatState.selectedText
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add assistant message to chat
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        citations: data.source_citations,
      };

      setChatState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        isLoading: false,
        selectedText: null, // Clear selected text after submission
      }));
    } catch (error) {
      console.error('Error fetching response:', error);
      
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };

      setChatState(prev => ({
        ...prev,
        messages: [...prev.messages, errorMessage],
        isLoading: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      }));
    }
  };

  const handleAskAboutSelection = async () => {
    if (!chatState.selectedText || chatState.isLoading) return;

    // Add user message to chat for the selected text query
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: `About the selected text: "${chatState.selectedText.substring(0, 100)}${chatState.selectedText.length > 100 ? '...' : ''}"`,
      timestamp: new Date(),
    };

    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: undefined
    }));

    try {
      // Call the backend API with selected context
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: 'Can you explain this text or answer a question about it?',
          selected_context: chatState.selectedText
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add assistant message to chat
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        citations: data.source_citations,
      };

      setChatState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        isLoading: false,
        selectedText: null, // Clear selected text after submission
      }));
    } catch (error) {
      console.error('Error fetching response:', error);
      
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };

      setChatState(prev => ({
        ...prev,
        messages: [...prev.messages, errorMessage],
        isLoading: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      }));
    }
  };

  return (
    <div className="rag-chatbot-container">
      <div className="rag-chatbot-header">
        <h3>RAG Chatbot</h3>
        {chatState.selectedText && (
          <div className="selected-text-preview">
            <p><strong>Selected text:</strong> "{chatState.selectedText.substring(0, 80)}{chatState.selectedText.length > 80 ? '...' : ''}"</p>
            <button 
              className="ask-about-selection-btn"
              onClick={handleAskAboutSelection}
              disabled={chatState.isLoading}
            >
              Ask about selection
            </button>
          </div>
        )}
      </div>
      
      <div className="rag-chatbot-messages">
        {chatState.messages.map((message) => (
          <div 
            key={message.id} 
            className={`message ${message.role}`}
          >
            <div className="message-content">
              {message.content}
            </div>
            {message.citations && message.citations.length > 0 && (
              <div className="citations">
                <strong>Sources:</strong>
                <ul>
                  {message.citations.map((citation, index) => (
                    <li key={index}>{citation}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
        {chatState.isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <em>Thinking...</em>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSubmit} className="rag-chatbot-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the documentation..."
          disabled={chatState.isLoading}
        />
        <button 
          type="submit" 
          disabled={!inputValue.trim() || chatState.isLoading}
        >
          Send
        </button>
      </form>
      
      {chatState.error && (
        <div className="error-message">
          Error: {chatState.error}
        </div>
      )}
    </div>
  );
};

export default RAGChatbot;