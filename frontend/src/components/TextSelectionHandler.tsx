import React, { useEffect } from 'react';

interface TextSelectionHandlerProps {
  setSelectedText: (text: string | null) => void;
}

export const TextSelectionHandler: React.FC<TextSelectionHandlerProps> = ({ setSelectedText }) => {
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim() !== '') {
        const selectedText = selection.toString().trim();
        if (selectedText.length > 0) {
          setSelectedText(selectedText);
        }
      } else {
        // Clear selection if no text is selected
        setSelectedText(null);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('touchend', handleSelection);
    };
  }, [setSelectedText]);

  return null; // This component doesn't render anything
};