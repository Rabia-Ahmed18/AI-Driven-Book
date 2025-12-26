import { useState } from 'react';

export const useTextSelection = () => {
  const [selectedText, setSelectedText] = useState<string | null>(null);

  const clearSelection = () => {
    setSelectedText(null);
  };

  return {
    selectedText,
    setSelectedText,
    clearSelection
  };
};