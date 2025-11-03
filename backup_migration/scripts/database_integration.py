"""
Database integration for demand forecasting system.
Supports SQLite and PostgreSQL for persistent storage.
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import sqlite3
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False

try:
    import psycopg2
    from psycopg2.extras import Json
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

import pandas as pd
import warnings
warnings.filterwarnings('ignore')


class DatabaseManager:
    """Database manager for forecasts and inventory."""
    
    def __init__(self, db_type: str = 'sqlite', connection_string: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            db_type: 'sqlite' or 'postgres'
            connection_string: Database connection string (optional for SQLite)
        """
        self.db_type = db_type.lower()
        self.connection_string = connection_string
        self.conn = None
        
        if self.db_type == 'sqlite':
            if not SQLITE_AVAILABLE:
                raise ImportError("SQLite not available")
            if connection_string is None:
                connection_string = 'data/forecasting.db'
            self.connection_string = connection_string
        
        elif self.db_type == 'postgres':
            if not POSTGRES_AVAILABLE:
                raise ImportError("PostgreSQL driver (psycopg2) not available")
            if connection_string is None:
                raise ValueError("PostgreSQL connection string required")
        
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    def connect(self):
        """Connect to database."""
        if self.db_type == 'sqlite':
            # Create directory if needed
            Path(self.connection_string).parent.mkdir(exist_ok=True, parents=True)
            self.conn = sqlite3.connect(self.connection_string)
            self.conn.row_factory = sqlite3.Row
        
        elif self.db_type == 'postgres':
            self.conn = psycopg2.connect(self.connection_string)
        
        self.create_tables()
    
    def create_tables(self):
        """Create database tables."""
        cursor = self.conn.cursor()
        
        if self.db_type == 'sqlite':
            # Forecasts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS forecasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id TEXT NOT NULL,
                    forecast_date DATE NOT NULL,
                    forecast_value REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    model_type TEXT,
                    metadata TEXT
                )
            """)
            
            # Inventory metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    current_stock REAL NOT NULL,
                    reorder_point REAL NOT NULL,
                    safety_stock REAL NOT NULL,
                    avg_daily_demand REAL NOT NULL,
                    days_to_rupture REAL,
                    lead_time INTEGER,
                    service_level REAL,
                    metadata TEXT,
                    UNIQUE(item_id, timestamp)
                )
            """)
            
            # Alerts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    alert_triggered BOOLEAN NOT NULL,
                    urgency TEXT,
                    message TEXT,
                    units_needed INTEGER,
                    metadata TEXT
                )
            """)
        
        elif self.db_type == 'postgres':
            # Forecasts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS forecasts (
                    id SERIAL PRIMARY KEY,
                    item_id VARCHAR(100) NOT NULL,
                    forecast_date DATE NOT NULL,
                    forecast_value REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    model_type VARCHAR(50),
                    metadata JSONB
                )
            """)
            
            # Inventory metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory_metrics (
                    id SERIAL PRIMARY KEY,
                    item_id VARCHAR(100) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    current_stock REAL NOT NULL,
                    reorder_point REAL NOT NULL,
                    safety_stock REAL NOT NULL,
                    avg_daily_demand REAL NOT NULL,
                    days_to_rupture REAL,
                    lead_time INTEGER,
                    service_level REAL,
                    metadata JSONB,
                    UNIQUE(item_id, timestamp)
                )
            """)
            
            # Alerts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id SERIAL PRIMARY KEY,
                    item_id VARCHAR(100) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    alert_triggered BOOLEAN NOT NULL,
                    urgency VARCHAR(20),
                    message TEXT,
                    units_needed INTEGER,
                    metadata JSONB
                )
            """)
        
        self.conn.commit()
    
    def save_forecast(self, item_id: str, forecast_data: pd.Series, 
                     model_type: str = 'ensemble', metadata: Optional[Dict] = None):
        """Save forecast to database."""
        cursor = self.conn.cursor()
        
        for date, value in forecast_data.items():
            if isinstance(date, str):
                date = pd.to_datetime(date).date()
            elif hasattr(date, 'date'):
                date = date.date()
            
            meta_json = json.dumps(metadata) if metadata else None
            
            if self.db_type == 'sqlite':
                cursor.execute("""
                    INSERT INTO forecasts 
                    (item_id, forecast_date, forecast_value, model_type, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (item_id, date, float(value), model_type, meta_json))
            
            elif self.db_type == 'postgres':
                cursor.execute("""
                    INSERT INTO forecasts 
                    (item_id, forecast_date, forecast_value, model_type, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                """, (item_id, date, float(value), model_type, 
                      Json(metadata) if metadata else None))
        
        self.conn.commit()
    
    def save_inventory_metrics(self, item_id: str, metrics: Dict, 
                               metadata: Optional[Dict] = None):
        """Save inventory metrics to database."""
        cursor = self.conn.cursor()
        
        meta_json = json.dumps(metadata) if metadata else None
        
        if self.db_type == 'sqlite':
            cursor.execute("""
                INSERT OR REPLACE INTO inventory_metrics
                (item_id, current_stock, reorder_point, safety_stock, 
                 avg_daily_demand, days_to_rupture, lead_time, service_level, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item_id,
                metrics['current_stock'],
                metrics['reorder_point'],
                metrics['safety_stock'],
                metrics['avg_daily_demand'],
                metrics['days_to_rupture'],
                metrics['lead_time'],
                metrics['service_level'],
                meta_json
            ))
        
        elif self.db_type == 'postgres':
            cursor.execute("""
                INSERT INTO inventory_metrics
                (item_id, current_stock, reorder_point, safety_stock, 
                 avg_daily_demand, days_to_rupture, lead_time, service_level, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (item_id, timestamp) DO UPDATE SET
                    current_stock = EXCLUDED.current_stock,
                    reorder_point = EXCLUDED.reorder_point,
                    safety_stock = EXCLUDED.safety_stock,
                    avg_daily_demand = EXCLUDED.avg_daily_demand,
                    days_to_rupture = EXCLUDED.days_to_rupture,
                    lead_time = EXCLUDED.lead_time,
                    service_level = EXCLUDED.service_level,
                    metadata = EXCLUDED.metadata
            """, (
                item_id,
                metrics['current_stock'],
                metrics['reorder_point'],
                metrics['safety_stock'],
                metrics['avg_daily_demand'],
                metrics['days_to_rupture'],
                metrics['lead_time'],
                metrics['service_level'],
                Json(metadata) if metadata else None
            ))
        
        self.conn.commit()
    
    def save_alert(self, item_id: str, alert: Dict, metadata: Optional[Dict] = None):
        """Save alert to database."""
        cursor = self.conn.cursor()
        
        meta_json = json.dumps(metadata) if metadata else None
        
        if self.db_type == 'sqlite':
            cursor.execute("""
                INSERT INTO alerts
                (item_id, alert_triggered, urgency, message, units_needed, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item_id,
                alert['alert_triggered'],
                alert['urgency'],
                alert['message'],
                alert['units_needed'],
                meta_json
            ))
        
        elif self.db_type == 'postgres':
            cursor.execute("""
                INSERT INTO alerts
                (item_id, alert_triggered, urgency, message, units_needed, metadata)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                item_id,
                alert['alert_triggered'],
                alert['urgency'],
                alert['message'],
                alert['units_needed'],
                Json(metadata) if metadata else None
            ))
        
        self.conn.commit()
    
    def get_latest_forecast(self, item_id: str) -> Optional[pd.DataFrame]:
        """Get latest forecast for item."""
        cursor = self.conn.cursor()
        
        if self.db_type == 'sqlite':
            cursor.execute("""
                SELECT forecast_date, forecast_value
                FROM forecasts
                WHERE item_id = ?
                ORDER BY created_at DESC, forecast_date ASC
                LIMIT 30
            """, (item_id,))
        else:
            cursor.execute("""
                SELECT forecast_date, forecast_value
                FROM forecasts
                WHERE item_id = %s
                ORDER BY created_at DESC, forecast_date ASC
                LIMIT 30
            """, (item_id,))
        
        rows = cursor.fetchall()
        
        if rows:
            df = pd.DataFrame(rows, columns=['forecast_date', 'forecast_value'])
            df['forecast_date'] = pd.to_datetime(df['forecast_date'])
            df.set_index('forecast_date', inplace=True)
            return df['forecast_value']
        
        return None
    
    def get_latest_inventory(self, item_id: str) -> Optional[Dict]:
        """Get latest inventory metrics for item."""
        cursor = self.conn.cursor()
        
        if self.db_type == 'sqlite':
            cursor.execute("""
                SELECT * FROM inventory_metrics
                WHERE item_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            """, (item_id,))
        else:
            cursor.execute("""
                SELECT * FROM inventory_metrics
                WHERE item_id = %s
                ORDER BY timestamp DESC
                LIMIT 1
            """, (item_id,))
        
        row = cursor.fetchone()
        
        if row:
            if self.db_type == 'sqlite':
                return dict(row)
            else:
                return dict(row)
        
        return None
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


if __name__ == '__main__':
    # Example usage
    with DatabaseManager('sqlite') as db:
        print("[OK] Database initialized")
        
        # Test save
        test_forecast = pd.Series([10, 12, 11, 13, 10], 
                                 index=pd.date_range(start='2024-01-01', periods=5, freq='D'))
        db.save_forecast('TEST-001', test_forecast)
        print("[OK] Forecast saved")
        
        # Test retrieve
        forecast = db.get_latest_forecast('TEST-001')
        if forecast is not None:
            print(f"[OK] Retrieved forecast: {len(forecast)} values")
        else:
            print("[WARNING] No forecast found")

