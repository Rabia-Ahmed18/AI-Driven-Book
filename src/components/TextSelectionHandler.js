import React, { useState, useEffect } from 'react';

const TextSelectionHandler = ({ setSelectedText }) => {
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const selectedText = selection.toString().trim();

      if (selectedText) {
        // Only set selected text if it's substantial (more than 5 characters)
        if (selectedText.length > 5) {
          setSelectedText(selectedText);
        }
      } else {
        setSelectedText(null);
      }
    };

    // Add event listeners for text selection
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    // Cleanup event listeners on component unmount
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, [setSelectedText]);

  return null; // This component doesn't render anything itself
};

export default TextSelectionHandler;