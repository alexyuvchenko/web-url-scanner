"""
Logging configuration for the URL Scanner.
"""

import logging
from pathlib import Path

from src.web_url_scanner.config import LOGS_DIR


def setup_logger(log_file: str = "scanner.log") -> logging.Logger:
    """
    Configure and return a logger instance.

    Args:
        log_file: Path to the log file. Defaults to 'scanner.log'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Use the logs directory from config
    log_path = LOGS_DIR / log_file

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_path)],
    )

    return logging.getLogger(__name__)
