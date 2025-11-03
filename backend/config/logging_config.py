"""
Logging configuration for Nova Corrente services
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Log directory
LOG_DIR = Path(os.getenv('LOG_DIR', 'logs'))
LOG_DIR.mkdir(exist_ok=True)

# Log levels
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# Log format
LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# File handler configuration
LOG_FILE_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_FILE_BACKUP_COUNT = 5

# Logger names for different modules
LOGGER_NAMES = {
    'database': 'nova_corrente.database',
    'features': 'nova_corrente.features',
    'ml_models': 'nova_corrente.ml_models',
    'etl': 'nova_corrente.etl',
    'algorithms': 'nova_corrente.algorithms',
    'api': 'nova_corrente.api',
}


def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Set up a logger with file and console handlers
    
    Args:
        name: Logger name
        log_file: Optional log file name (defaults to {name}.log)
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LOG_FORMAT)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file is None:
        log_file = f"{name.replace('.', '_')}.log"
    
    file_path = LOG_DIR / log_file
    file_handler = RotatingFileHandler(
        file_path,
        maxBytes=LOG_FILE_MAX_BYTES,
        backupCount=LOG_FILE_BACKUP_COUNT
    )
    file_handler.setFormatter(LOG_FORMAT)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger for the given name"""
    return setup_logger(name)

