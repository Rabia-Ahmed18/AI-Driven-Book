import React, { useEffect } from 'react';
import { useTextSelection } from '../hooks/useTextSelection';

export const TextSelectionHandler: React.FC = () => {
  const { setSelectedText } = useTextSelection();

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim() !== '') {
        const selectedText = selection.toString().trim();
        if (selectedText.length > 0) {
          setSelectedText(selectedText);
        }
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