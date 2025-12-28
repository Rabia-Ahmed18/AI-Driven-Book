import React, { useState, useEffect } from 'react';
import './SelectionButton.css';

const SelectionButton = ({ onSelection, selectedText }) => {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection.toString().trim() !== '') {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        
        // Position the button near the selection
        setPosition({
          x: rect.left + rect.width / 2,
          y: rect.top - 40
        });
        
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  const handleClick = () => {
    const selection = window.getSelection().toString().trim();
    if (selection) {
      onSelection(selection);
      setIsVisible(false);
    }
  };

  if (!isVisible || !selectedText) {
    return null;
  }

  return (
    <button
      className="selection-button"
      style={{
        position: 'fixed',
        left: `${position.x}px`,
        top: `${position.y}px`,
        transform: 'translateX(-50%)',
        zIndex: 10000
      }}
      onClick={handleClick}
    >
      💬 Ask AI
    </button>
  );
};

export default SelectionButton;