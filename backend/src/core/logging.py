import logging
import sys
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


import os


def setup_logging(name: str = "rag_chatbot", level: LogLevel = LogLevel.INFO):
    """
    Set up logging configuration for the application
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.value))

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.value))

    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Create file handler
    file_handler = logging.FileHandler(f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler.setLevel(getattr(logging, level.value))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


def log_exception(logger, exc: Exception, context: str = ""):
    """
    Log exception with context
    """
    logger.error(f"Exception in {context}: {str(exc)}", exc_info=True)


# Global logger instance
app_logger = setup_logging()