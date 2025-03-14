import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(log_dir: str = "logs") -> logging.Logger:
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)
    
    # Configure the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Log format
    log_format = logging.Formatter(
        "[%(asctime)s] - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File handler with rotation (10MB max size, keep 5 backup files)
    file_handler = RotatingFileHandler(
        f"{log_dir}/app.log",
        maxBytes=10_000_000,
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    
    # Error file handler
    error_handler = RotatingFileHandler(
        f"{log_dir}/error.log",
        maxBytes=10_000_000,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

# Usage example:
# logger.debug("Debug message")
# logger.info("Info message")
# logger.warning("Warning message")
# logger.error("Error message")
# logger.critical("Critical message")