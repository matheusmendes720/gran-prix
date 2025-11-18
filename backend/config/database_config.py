"""
Database configuration for Nova Corrente ML-ready database
"""
import os
from typing import Dict, Any

# Database connection settings
DATABASE_CONFIG: Dict[str, Any] = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'STOCK'),
    'charset': 'utf8mb4',
    'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
    'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 20)),
    'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', 30)),
    'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
    'echo': os.getenv('DB_ECHO', 'False').lower() == 'true',
}

# SQLAlchemy connection string
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
    f"?charset={DATABASE_CONFIG['charset']}"
)

# Async MySQL connection string
ASYNC_DATABASE_URI = (
    f"mysql+aiomysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
    f"?charset={DATABASE_CONFIG['charset']}"
)

# Query timeout settings
QUERY_TIMEOUT = int(os.getenv('QUERY_TIMEOUT', 30))  # seconds

# Transaction isolation level
ISOLATION_LEVEL = os.getenv('DB_ISOLATION_LEVEL', 'READ_COMMITTED')

