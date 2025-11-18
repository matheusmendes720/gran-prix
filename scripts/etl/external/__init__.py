"""
Utility package for external data ingestion scripts.

Contains helper functions and clients used to download macroeconomic,
climatic and logistics indicators that feed Nova Corrente forecasting pipelines.
"""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(name: str) -> logging.Logger:
    """Return a logger pre-configured with console handler."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def ensure_directory(path: Path) -> Path:
    """Create a directory if it does not exist and return the path."""
    path.mkdir(parents=True, exist_ok=True)
    return path

