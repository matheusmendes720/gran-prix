#!/usr/bin/env python3
"""
Standalone script to run the FastAPI server
Handles proper path setup and service initialization
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
project_root = backend_dir.parent

# Add project root first, then backend
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Set environment variables if needed
os.environ.setdefault('PYTHONPATH', str(backend_dir))

if __name__ == "__main__":
    import uvicorn
    
    # Try to load .env, but don't fail if it doesn't exist or has issues
    try:
        from dotenv import load_dotenv
        # Load with encoding and ignore parsing errors
        load_dotenv(encoding='utf-8', override=False)
    except Exception as e:
        # Silently ignore .env parsing errors - they're not critical
        pass
    
    # Import after path setup
    try:
        from app.config import settings
        api_host = settings.API_HOST
        api_port = settings.API_PORT
        api_reload = settings.API_RELOAD
    except Exception as e:
        print(f"Warning: Could not load settings: {e}")
        print("Using default values...")
        api_host = os.getenv("API_HOST", "127.0.0.1")
        api_port = int(os.getenv("API_PORT", "5000"))
        api_reload = os.getenv("API_RELOAD", "true").lower() == "true"
    
    print("=" * 60)
    print("Starting Nova Corrente API Server")
    print("=" * 60)
    print(f"Host: {api_host}")
    print(f"Port: {api_port}")
    print(f"Reload: {api_reload}")
    print(f"Docs: http://{api_host}:{api_port}/docs")
    print("=" * 60)
    print()
    
    try:
        uvicorn.run(
            "app.main:app",
            host=api_host,
            port=api_port,
            reload=api_reload,
            log_level="info",
        )
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"\nError starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

