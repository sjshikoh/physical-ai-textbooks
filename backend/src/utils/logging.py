import logging
import sys
from datetime import datetime
from typing import Any, Dict
from .config import config

# Configure the root logger
def setup_logging():
    """
    Set up logging configuration for the application
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
    root_logger.addHandler(console_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("qdrant_client").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.INFO)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name

    Args:
        name: Name of the logger

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


class AppException(Exception):
    """
    Base application exception class
    """
    def __init__(self, message: str, status_code: int = 500, details: Dict[str, Any] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary for API responses
        """
        return {
            "error": self.message,
            "status_code": self.status_code,
            "details": self.details,
            "timestamp": datetime.utcnow().isoformat()
        }


class RAGException(AppException):
    """
    Exception for RAG-related errors
    """
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, 500, details)


class TextbookException(AppException):
    """
    Exception for textbook-related errors
    """
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, 404, details)


class ValidationException(AppException):
    """
    Exception for validation errors
    """
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, 400, details)


# Initialize logging
logger = setup_logging()