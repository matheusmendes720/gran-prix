import os
from typing import Dict, Any

# Database configuration
DATABASE_CONFIG: Dict[str, Any] = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'nova_corrente'),
    'password': os.getenv('DB_PASSWORD', 'strong_password'),
    'database': os.getenv('DB_NAME', 'nova_corrente'),
    'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
    'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 20)),
    'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', 30)),
    'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
    'echo': os.getenv('DB_ECHO', 'False').lower() == 'true',
}

# PostgreSQL connection string
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)