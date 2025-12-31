import React, { useState } from 'react';
import { RagChatbot } from './components/RagChatbot';
import { TextSelectionHandler } from './components/TextSelectionHandler';

function App() {
  const [selectedText, setSelectedText] = useState<string | null>(null);

  return (
    <div className="App">
      <TextSelectionHandler setSelectedText={setSelectedText} />
      <header className="App-header">
        <h1>AI-Powered Book Assistant</h1>
      </header>
      <main>
        <div className="app-layout">
          <div className="book-content">
            <h2>Sample Book Content</h2>
            <p>Select some text in this content to ask questions about it.</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
            <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
            <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.</p>
            <p>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.</p>
          </div>
          <div className="chatbot-container">
            <RagChatbot bookId="sample-book-id" selectedText={selectedText} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;