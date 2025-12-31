import React, { useState, useEffect, useRef } from 'react';
import './ChatWidget.css';

const ChatWidget = ({ selectedText = '', onUseSelection = null }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [currentSelectedText, setCurrentSelectedText] = useState('');
  const messagesEndRef = useRef(null);

  // Handle selected text prop changes
  useEffect(() => {
    if (selectedText) {
      setCurrentSelectedText(selectedText);
    }
  }, [selectedText]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Function to handle sending a message
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the request payload
      const requestBody = {
        question: inputValue,
        session_id: sessionId || undefined,
        selected_text: currentSelectedText || undefined
      };

      // Make API call to backend
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update session ID if it's the first message
      if (!sessionId) {
        setSessionId(data.session_id);
      }

      // Add bot response to the chat
      const botMessage = {
        id: Date.now() + 1,
        text: data.answer,
        sender: 'bot',
        sources: data.sources,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        error: true,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setCurrentSelectedText(''); // Clear selected text after sending
    }
  };

  // Handle key press (Enter to send)
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Toggle chat widget open/close
  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Clear chat history
  const clearChat = () => {
    setMessages([]);
    setCurrentSelectedText(''); // Also clear any selected text
  };

  // Handle using the selected text
  const handleUseSelection = () => {
    if (selectedText && onUseSelection) {
      onUseSelection(selectedText);
      setCurrentSelectedText(selectedText);
      setIsOpen(true); // Open the chat if it's closed
    }
  };

  return (
    <div className="chat-widget">
      {isOpen ? (
        <div className="chat-container">
          <div className="chat-header">
            <div className="chat-title">
              {currentSelectedText ? 'Answering based on selection...' : 'Book Assistant'}
            </div>
            <div className="chat-controls">
              <button onClick={clearChat} className="clear-btn" title="Clear chat">
                ✕
              </button>
              <button onClick={toggleChat} className="close-btn" title="Close chat">
                −
              </button>
            </div>
          </div>

          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <p>Hello! I'm your Assistant buddy.</p>
                {currentSelectedText && (
                  <p className="selected-text-preview">
                    <strong>Context:</strong> "{currentSelectedText.substring(0, 50)}{currentSelectedText.length > 50 ? '...' : ''}"
                  </p>
                )}
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
                >
                  <div className="message-text">
                    {message.text}
                  </div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                      <details>
                        <summary>Sources</summary>
                        <ul>
                          {message.sources.map((source, index) => (
                            <li key={index}>
                              <a href={source.url} target="_blank" rel="noopener noreferrer">
                                {source.heading || 'Reference'}
                              </a>
                            </li>
                          ))}
                        </ul>
                      </details>
                    </div>
                  )}
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-text">
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
            {currentSelectedText && (
              <div className="selected-text-indicator">
                Using selected text as context: "{currentSelectedText.substring(0, 60)}{currentSelectedText.length > 60 ? '...' : ''}"
              </div>
            )}
            <div className="input-container">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={currentSelectedText
                  ? "Ask about the selected text..."
                  : "Ask a question about the book..."}
                className="chat-input"
                rows="1"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputValue.trim()}
                className="send-button"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      ) : (
        <button className="chat-toggle-button" onClick={toggleChat}>
          🙋🏻‍♂️
        </button>
      )}
      {selectedText && !isOpen && (
        <button
          className="use-selection-button"
          onClick={handleUseSelection}
          title="Use selected text in chat"
        >
          🙋🏻‍♂️Ask AI
        </button>
      )}
    </div>
  );
};

export default ChatWidget;