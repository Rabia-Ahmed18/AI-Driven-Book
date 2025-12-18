import logging
import sys
from typing import Any, Dict
from functools import wraps
from fastapi import HTTPException


def setup_logging(name: str, log_level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with the specified name and level
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid adding multiple handlers if logger already exists
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def log_exceptions(func):
    """
    Decorator to log exceptions in functions
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger = setup_logging(func.__module__)
            logger.error(f"Exception in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper


def handle_api_errors(status_code: int = 500, message: str = "Internal Server Error"):
    """
    Create an HTTPException with the given status code and message
    """
    return HTTPException(status_code=status_code, detail=message)