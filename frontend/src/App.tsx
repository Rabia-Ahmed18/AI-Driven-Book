import React from 'react';
import { RagChatbot } from './components/RagChatbot';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI-Powered Book Assistant</h1>
      </header>
      <main>
        <div className="book-content">
          <h2>Sample Book Content</h2>
          <p>Select some text in this content to ask questions about it.</p>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
          <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </div>
        <div className="chatbot-container">
          <RagChatbot bookId="sample-book-id" />
        </div>
      </main>
    </div>
  );
}

export default App;