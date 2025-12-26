from typing import Any
from pydantic import BaseModel, ValidationError, validator


def validate_input(data: Any, model: BaseModel) -> Any:
    """
    Validate input data against a Pydantic model
    """
    try:
        validated_data = model(**data)
        return validated_data
    except ValidationError as e:
        raise ValueError(f"Input validation failed: {e}")


def sanitize_text(text: str) -> str:
    """
    Sanitize text input to prevent injection attacks
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    # Remove potentially dangerous characters/sequences
    sanitized = text.replace('\0', '')  # Remove null bytes
    sanitized = sanitized.replace('\x00', '')  # Another way null bytes might be represented
    
    # Additional sanitization can be added here as needed
    
    return sanitized


def validate_book_content(content: str) -> bool:
    """
    Validate book content meets minimum requirements
    """
    if not content or len(content.strip()) < 50:
        raise ValueError("Book content is too short, minimum 50 characters required")
    
    # Check for potentially problematic content
    if len(content) > 1000000:  # 1MB limit
        raise ValueError("Book content is too large, maximum 1MB allowed")
    
    return True


def validate_user_query(query: str) -> bool:
    """
    Validate user query meets requirements
    """
    if not query or len(query.strip()) < 3:
        raise ValueError("Query is too short, minimum 3 characters required")
    
    if len(query) > 1000:  # 1000 character limit
        raise ValueError("Query is too long, maximum 1000 characters allowed")
    
    return True