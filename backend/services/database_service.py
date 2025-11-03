"""
Database service layer for Nova Corrente ML-ready database
Provides connection pooling, query builder, and transaction management
"""
from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

from backend.config.database_config import (
    SQLALCHEMY_DATABASE_URI,
    DATABASE_CONFIG,
    QUERY_TIMEOUT,
)
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.database')


class DatabaseService:
    """
    Singleton database service with connection pooling
    """
    _instance: Optional['DatabaseService'] = None
    _engine = None
    _SessionLocal = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._engine is None:
            self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize SQLAlchemy engine with connection pooling"""
        try:
            self._engine = create_engine(
                SQLALCHEMY_DATABASE_URI,
                poolclass=QueuePool,
                pool_size=DATABASE_CONFIG['pool_size'],
                max_overflow=DATABASE_CONFIG['max_overflow'],
                pool_timeout=DATABASE_CONFIG['pool_timeout'],
                pool_recycle=DATABASE_CONFIG['pool_recycle'],
                echo=DATABASE_CONFIG['echo'],
                connect_args={
                    'connect_timeout': QUERY_TIMEOUT,
                    'charset': 'utf8mb4',
                }
            )
            
            # Create session factory
            self._SessionLocal = scoped_session(
                sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=self._engine
                )
            )
            
            logger.info("Database engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise
    
    @property
    def engine(self):
        """Get database engine"""
        return self._engine
    
    def get_session(self) -> Session:
        """
        Get a database session
        
        Returns:
            Database session
        """
        if self._SessionLocal is None:
            self._initialize_engine()
        
        return self._SessionLocal()
    
    @contextmanager
    def transaction(self):
        """
        Context manager for database transactions
        
        Usage:
            with db_service.transaction() as session:
                # database operations
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Transaction error: {e}")
            raise
        finally:
            session.close()
    
    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        fetch_one: bool = False,
        fetch_all: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results
        
        Args:
            query: SQL query string
            params: Query parameters
            fetch_one: Return only first result
            fetch_all: Return all results (default True)
        
        Returns:
            Query results as list of dictionaries
        """
        try:
            with self._engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                
                if fetch_one:
                    row = result.fetchone()
                    return dict(row._mapping) if row else None
                
                if fetch_all:
                    rows = result.fetchall()
                    return [dict(row._mapping) for row in rows]
                
                return []
        except SQLAlchemyError as e:
            logger.error(f"Query execution error: {e}")
            raise
    
    def execute_raw_sql(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Execute raw SQL (INSERT, UPDATE, DELETE) and return affected rows
        
        Args:
            sql: SQL statement
            params: Query parameters
        
        Returns:
            Number of affected rows
        """
        try:
            with self._engine.connect() as connection:
                result = connection.execute(text(sql), params or {})
                connection.commit()
                return result.rowcount
        except SQLAlchemyError as e:
            logger.error(f"SQL execution error: {e}")
            raise
    
    def execute_procedure(
        self,
        procedure_name: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a stored procedure
        
        Args:
            procedure_name: Stored procedure name
            params: Procedure parameters
        
        Returns:
            Procedure results
        """
        try:
            # Build procedure call
            if params:
                param_str = ', '.join([f":{k}" for k in params.keys()])
                call_sql = f"CALL {procedure_name}({param_str})"
            else:
                call_sql = f"CALL {procedure_name}()"
            
            with self._engine.connect() as connection:
                result = connection.execute(text(call_sql), params or {})
                connection.commit()
                rows = result.fetchall()
                return [dict(row._mapping) for row in rows]
        except SQLAlchemyError as e:
            logger.error(f"Procedure execution error: {e}")
            raise
    
    def get_dataframe(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """
        Execute query and return as pandas DataFrame
        
        Args:
            query: SQL query
            params: Query parameters
        
        Returns:
            Query results as DataFrame
        """
        try:
            return pd.read_sql_query(query, self._engine, params=params)
        except Exception as e:
            logger.error(f"DataFrame query error: {e}")
            raise
    
    def insert_dataframe(
        self,
        table_name: str,
        df: pd.DataFrame,
        if_exists: str = 'append',
        index: bool = False
    ) -> int:
        """
        Insert DataFrame into database table
        
        Args:
            table_name: Target table name
            df: DataFrame to insert
            if_exists: 'fail', 'replace', or 'append'
            index: Write DataFrame index
        
        Returns:
            Number of rows inserted
        """
        try:
            rows_inserted = df.to_sql(
                table_name,
                self._engine,
                if_exists=if_exists,
                index=index,
                method='multi',
                chunksize=1000
            )
            logger.info(f"Inserted {len(df)} rows into {table_name}")
            return rows_inserted
        except Exception as e:
            logger.error(f"DataFrame insert error: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test database connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def close(self):
        """Close database connections"""
        if self._SessionLocal:
            self._SessionLocal.remove()
        if self._engine:
            self._engine.dispose()
        logger.info("Database connections closed")


# Singleton instance
db_service = DatabaseService()

