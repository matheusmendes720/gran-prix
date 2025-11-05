from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Any, Optional
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        # Use PostgreSQL database URL
        self.database_url = os.getenv(
            'DATABASE_URL', 
            'postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente'
        )
        
        # Create engine with connection pooling
        self.engine = create_engine(
            self.database_url,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=3600,
            echo=os.getenv('DB_ECHO', 'False').lower() == 'true'
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Get a database session"""
        return self.SessionLocal()
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results as list of dictionaries"""
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            return [dict(row._mapping) for row in result]
    
    def execute_single_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Execute a query and return a single result"""
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            row = result.fetchone()
            return dict(row._mapping) if row else None
    
    def execute_mutation(self, query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """Execute a mutation (INSERT, UPDATE, DELETE) and return affected rows"""
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            session.commit()
            return result.rowcount
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.get_session() as session:
                session.execute(text('SELECT 1'))
                return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

# Create a global instance
database_service = DatabaseService()