import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '../types';

interface ChatWindowProps {
  messages: ChatMessage[];
  onSend: (message: string) => void;
  isLoading: boolean;
  selectedText?: string | null;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ 
  messages, 
  onSend, 
  isLoading,
  selectedText 
}) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSend(inputValue);
      setInputValue('');
    }
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>Book Assistant</h3>
        {selectedText && selectedText.length > 0 && (
          <div className="selected-text-preview">
            <p><strong>Context:</strong> {selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}</p>
          </div>
        )}
      </div>
      
      <div className="chat-messages">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <div className="message-content">
              {message.content}
              {message.citations && message.citations.length > 0 && (
                <div className="citations">
                  <h4>Sources:</h4>
                  <ul>
                    {message.citations.map((citation, index) => (
                      <li key={index}>
                        <p>{citation.text}</p>
                        <small>Confidence: {(citation.confidence * 100).toFixed(1)}%</small>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the book..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};