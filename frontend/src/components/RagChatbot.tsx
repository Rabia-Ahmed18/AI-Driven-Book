import React, { useState, useEffect, useRef } from 'react';
import { ChatMessage } from '../types';
import { apiService } from '../services/api';
import { useChatState } from '../hooks/useChatState';
import './RagChatbot.css';

interface RagChatbotProps {
  bookId: string;
  selectedText?: string | null;
}

export const RagChatbot: React.FC<RagChatbotProps> = ({ bookId, selectedText }) => {
  const [inputValue, setInputValue] = useState('');
  const [isExpanded, setIsExpanded] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Use the custom chat state hook
  const [chatState, chatActions] = useChatState();

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [chatState.messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || chatState.isLoading) return;

    // Add user message to the chat
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputValue,
      role: 'user',
      timestamp: new Date()
    };

    chatActions.addMessage(userMessage);
    setInputValue('');
    chatActions.setIsLoading(true);
    chatActions.setError(null);

    try {
      const response = await apiService.chat({
        user_query: inputValue,
        book_id: bookId,
        selected_text: selectedText || undefined,
        session_id: chatState.sessionId || undefined
      });

      // Update session ID if it's the first message
      if (!chatState.sessionId && response.session_id) {
        chatActions.setSessionId(response.session_id);
      }

      // Add bot response to the chat
      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        role: 'assistant',
        timestamp: new Date(),
        citations: response.citations
      };

      chatActions.addMessage(botMessage);
    } catch (err) {
      console.error('Error sending message:', err);
      chatActions.setError('Failed to get response. Please try again.');

      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        timestamp: new Date()
      };

      chatActions.addMessage(errorMessage);
    } finally {
      chatActions.setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className={`rag-chatbot ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="chat-header" onClick={toggleExpand}>
        <h3><span className="icon">🤖</span> AI Book Assistant</h3>
        <div className="header-controls">
          <span className="expand-toggle">{isExpanded ? '−' : '+'}</span>
        </div>
      </div>

      {isExpanded && (
        <>
          <div className="chat-messages">
            {chatState.messages.length === 0 ? (
              <div className="welcome-message">
                <h4>Hello! I'm your AI book assistant.</h4>
                <p>Ask me anything about this book, and I'll provide answers based on the content.</p>
                {selectedText && (
                  <div className="context-preview">
                    <p><strong>Using context:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</p>
                  </div>
                )}
              </div>
            ) : (
              chatState.messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
                >
                  <div className="message-content">
                    {message.content}

                    {message.citations && message.citations.length > 0 && (
                      <div className="citations">
                        <details>
                          <summary>Sources ({message.citations.length})</summary>
                          <ul>
                            {message.citations.map((citation, index) => (
                              <li key={index} className="citation-item">
                                <p>{citation.text.substring(0, 150)}{citation.text.length > 150 ? '...' : ''}</p>
                                <small>Confidence: {(citation.confidence * 100).toFixed(1)}%</small>
                              </li>
                            ))}
                          </ul>
                        </details>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}

            {chatState.isLoading && (
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

          <div className="chat-input-area">
            {selectedText && (
              <div className="selected-text-indicator">
                <strong>Context:</strong> "{selectedText.substring(0, 60)}{selectedText.length > 60 ? '...' : ''}"
              </div>
            )}

            <div className="input-container">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={selectedText
                  ? "Ask about the selected text..."
                  : "Ask a question about the book..."}
                className="chat-input"
                rows={1}
                disabled={chatState.isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={chatState.isLoading || !inputValue.trim()}
                className="send-button"
              >
                {chatState.isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>

            {chatState.error && <div className="error-message">{chatState.error}</div>}
          </div>
        </>
      )}
    </div>
  );
};