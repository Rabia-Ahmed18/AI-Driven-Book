import re
from typing import List, Dict, Any


class TextSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Split text into chunks of specified size with overlap
        Returns list of dictionaries with content and metadata
        """
        # Split text by paragraphs first
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        current_metadata = {"start_pos": 0, "end_pos": 0}
        
        for para_idx, paragraph in enumerate(paragraphs):
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > self.chunk_size:
                # Save current chunk if it's substantial
                if len(current_chunk) > 100:  # Minimum chunk size
                    chunks.append({
                        "content": current_chunk.strip(),
                        "metadata": current_metadata.copy()
                    })
                
                # Start new chunk with overlap from previous chunk
                if len(paragraph) > self.chunk_size:
                    # If the paragraph itself is too large, split it
                    sub_chunks = self._split_large_paragraph(paragraph)
                    for sub_chunk in sub_chunks[:-1]:  # Add all but the last one
                        chunks.append({
                            "content": sub_chunk,
                            "metadata": {"para_idx": para_idx, "type": "sub_chunk"}
                        })
                    # Keep the last sub-chunk as the start of the next chunk
                    current_chunk = sub_chunks[-1]
                else:
                    # Start with some overlap from the previous chunk
                    if len(current_chunk) > self.chunk_overlap:
                        overlap = current_chunk[-self.chunk_overlap:]
                        current_chunk = overlap + " " + paragraph
                    else:
                        current_chunk = paragraph
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        # Add the final chunk if it's substantial
        if len(current_chunk) > 100:
            chunks.append({
                "content": current_chunk.strip(),
                "metadata": current_metadata.copy()
            })
        
        return chunks

    def _split_large_paragraph(self, paragraph: str) -> List[str]:
        """
        Split a large paragraph into smaller chunks
        """
        sentences = re.split(r'(?<=[.!?]) +', paragraph)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks


# Default text splitter instance
text_splitter = TextSplitter()