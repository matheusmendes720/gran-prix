"""
Utility module for project path resolution
"""

from pathlib import Path

def get_project_root() -> Path:
    """Get project root directory (3 levels up from src/utils)"""
    return Path(__file__).parent.parent.parent

PROJECT_ROOT = get_project_root()

# Common paths
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
TRAINING_DATA_DIR = DATA_DIR / "training"
REPORTS_DIR = DATA_DIR / "reports"

