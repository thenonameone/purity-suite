"""
Logging utilities for the geolocalization system.
"""

import os
import sys
from loguru import logger
from typing import Optional


def setup_logger(log_level: str = "INFO", 
                log_file: Optional[str] = None,
                log_format: Optional[str] = None) -> None:
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
        log_format: Optional custom log format
    """
    # Remove default logger
    logger.remove()
    
    # Default format if none provided
    if log_format is None:
        log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    
    # Add console handler
    logger.add(
        sys.stderr,
        format=log_format,
        level=log_level,
        colorize=True
    )
    
    # Add file handler if specified
    if log_file:
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        logger.add(
            log_file,
            format=log_format,
            level=log_level,
            rotation="10 MB",  # Rotate when file reaches 10MB
            retention="1 month",  # Keep logs for 1 month
            compression="zip"  # Compress rotated logs
        )
    
    logger.info(f"Logger initialized with level: {log_level}")
    if log_file:
        logger.info(f"Logging to file: {log_file}")


def get_logger(name: str = __name__):
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logger.bind(name=name)