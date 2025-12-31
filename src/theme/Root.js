import React, { useState, useEffect } from 'react';
import ChatWidget from '@site/src/components/ChatWidget';
import TextSelectionHandler from '@site/src/components/TextSelectionHandler';

export default function Root({ children }) {
  // Only load the chatbot in browser environment
  const [isBrowser, setIsBrowser] = React.useState(false);
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    setIsBrowser(typeof window !== 'undefined');
  }, []);

  return (
    <>
      {children}
      {isBrowser && (
        <>
          <TextSelectionHandler setSelectedText={setSelectedText} />
          <ChatWidget selectedText={selectedText} />
        </>
      )}
    </>
  );
}