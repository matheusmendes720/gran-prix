"""
Path fixing utility for imports
Ensures backend module can be found regardless of execution path
"""
import sys
from pathlib import Path

def setup_backend_path():
    """Add backend directory to Python path"""
    # Get backend directory (parent of app directory)
    current_file = Path(__file__)
    backend_dir = current_file.parent.parent.parent
    
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    
    return backend_dir

# Auto-setup on import
setup_backend_path()









