#!/usr/bin/env python3
"""
Run the Flask enhanced API server
"""
import sys
import os
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent
project_root = backend_dir.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

if __name__ == '__main__':
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv(backend_dir / '.env')
    except:
        pass
    
    # Import the Flask app
    from backend.api.enhanced_api import app
    
    host = os.getenv('API_HOST', '127.0.0.1')
    port = int(os.getenv('API_PORT', '5000'))
    debug = os.getenv('API_RELOAD', 'false').lower() == 'true'
    
    print("=" * 60)
    print("🚀 Nova Corrente Flask API Server")
    print("=" * 60)
    print(f"📡 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🐛 Debug: {debug}")
    print(f"📚 Health: http://{host}:{port}/health")
    print(f"📊 API v1: http://{host}:{port}/api/v1/")
    print("=" * 60)
    print()
    
    app.run(host=host, port=port, debug=debug)
