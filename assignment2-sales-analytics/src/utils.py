"""
Utility functions for logging and error handling.
Non-intrusive utilities for robustness without adding complexity.
"""

import logging
import os
from functools import wraps
from typing import Callable, Any


def setup_logger(name: str) -> logging.Logger:
    """
    Configure logging with appropriate format.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance

    FP Principle: Pure function (same input = same output structure)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def safe_execute(fn: Callable, *args, **kwargs) -> tuple[bool, Any]:
    """
    Error-wrapped function execution.
    Returns (success, result) tuple for functional error handling.

    Args:
        fn: Function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Tuple of (success: bool, result: Any | Exception)

    FP Principle: Higher-order function (takes function as parameter)
    """
    try:
        result = fn(*args, **kwargs)
        return (True, result)
    except Exception as e:
        return (False, e)


def validate_csv_file(filepath: str) -> tuple[bool, str]:
    """
    Check file existence and format.
    Pure function for file validation.

    Args:
        filepath: Path to CSV file

    Returns:
        Tuple of (is_valid: bool, message: str)

    FP Principle: Pure function with no side effects
    """
    if not os.path.exists(filepath):
        return (False, f"File not found: {filepath}")

    if not filepath.endswith('.csv'):
        return (False, f"Not a CSV file: {filepath}")

    file_size = os.path.getsize(filepath)
    if file_size == 0:
        return (False, f"File is empty: {filepath}")

    return (True, f"Valid CSV file: {filepath} ({file_size / (1024*1024):.2f} MB)")


def log_analysis(analysis_name: str, result_count: int) -> None:
    """
    Log analysis execution.
    Simple logging wrapper without complexity.

    Args:
        analysis_name: Name of the analysis
        result_count: Number of results produced

    FP Principle: Minimal side effects (logging only)
    """
    logger = setup_logger(__name__)
    logger.info(f"Analysis '{analysis_name}' completed with {result_count} results")


def with_error_handling(logger_name: str = __name__):
    """
    Decorator for error handling with logging.

    Args:
        logger_name: Name for the logger

    Returns:
        Decorator function

    FP Principle: Decorator pattern (higher-order function)
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            logger = setup_logger(logger_name)
            try:
                result = fn(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error in {fn.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator
