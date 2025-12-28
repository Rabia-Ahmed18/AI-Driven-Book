import os
import re
from typing import List, Dict, Any
from pathlib import Path
from ..core.logging import app_logger


class DocumentParser:
    """
    Service for parsing documents from various formats
    Currently supports Markdown (.md) and MDX (.mdx) files
    """
    
    def __init__(self):
        pass
    
    def parse_markdown_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a markdown file and extract content with metadata
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from the first heading
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else Path(file_path).stem
            
            # Extract other metadata if available (frontmatter, etc.)
            metadata = self._extract_frontmatter(content)
            
            return {
                "title": title,
                "content": content,
                "metadata": metadata,
                "file_path": file_path
            }
        except Exception as e:
            app_logger.error(f"Error parsing markdown file {file_path}: {str(e)}")
            raise
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        Extract frontmatter from markdown content if present
        """
        frontmatter = {}
        # Look for YAML frontmatter at the beginning of the file
        if content.startswith('---'):
            try:
                end_marker = content.find('---', 3)  # Find the closing ---
                if end_marker != -1:
                    frontmatter_content = content[3:end_marker].strip()
                    # Simple YAML-like parsing (for basic key-value pairs)
                    for line in frontmatter_content.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            frontmatter[key.strip()] = value.strip().strip('"\'')
            except Exception:
                # If frontmatter parsing fails, continue without it
                app_logger.warning(f"Could not parse frontmatter in document")
        
        return frontmatter
    
    def parse_mdx_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse an MDX file (Markdown with JSX) and extract content with metadata
        For now, treat MDX files similarly to markdown files
        """
        return self.parse_markdown_file(file_path)
    
    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a document based on its file extension
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.md':
            return self.parse_markdown_file(file_path)
        elif file_ext == '.mdx':
            return self.parse_mdx_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
    
    def get_all_documents(self, directory_path: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """
        Get all supported documents from a directory
        """
        documents = []
        patterns = ["*.md", "*.mdx"]
        
        for pattern in patterns:
            if recursive:
                file_paths = Path(directory_path).rglob(pattern)
            else:
                file_paths = Path(directory_path).glob(pattern)
            
            for file_path in file_paths:
                try:
                    doc = self.parse_document(str(file_path))
                    documents.append(doc)
                except Exception as e:
                    app_logger.error(f"Error parsing document {file_path}: {str(e)}")
        
        return documents


# Global instance
document_parser = DocumentParser()