"""
Text Splitter Utility for RAG-Based AI Book Chatbot

This module provides utilities for splitting text content into chunks
using RecursiveCharacterTextSplitter from langchain.
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List


class TextSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        """
        Initialize the text splitter with specified parameters.
        
        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Overlap between consecutive chunks to maintain context
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize the RecursiveCharacterTextSplitter
        # This splits text by different characters in a hierarchy:
        # 1. Split by \n\n (paragraphs)
        # 2. Split by \n (newlines)
        # 3. Split by " " (spaces)
        # 4. Split by "" (characters)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )
    
    def split_text(self, text: str) -> List[str]:
        """
        Split the input text into chunks.
        
        Args:
            text: Input text to be split
            
        Returns:
            List of text chunks
        """
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    def split_text_with_metadata(self, text: str, metadata: dict = None) -> List[dict]:
        """
        Split the input text into chunks with associated metadata.
        
        Args:
            text: Input text to be split
            metadata: Metadata to be associated with each chunk
            
        Returns:
            List of dictionaries containing 'content' and 'metadata'
        """
        if metadata is None:
            metadata = {}
        
        chunks = self.text_splitter.split_text(text)
        result = []
        
        for chunk in chunks:
            result.append({
                "content": chunk,
                "metadata": metadata.copy()
            })
        
        return result