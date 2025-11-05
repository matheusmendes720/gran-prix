# etl/run_kpi_calculations.py
import os
from sqlalchemy import create_engine, text
from datetime import datetime

def run_kpi_calculations():
    print("Starting KPI Calculations...")
    
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente')
    engine = create_engine(DATABASE_URL)
    
    # Read the SQL file
    with open('etl/calculate_kpis.sql', 'r') as f:
        sql_content = f.read()
    
    # Execute the KPI calculation
    with engine.connect() as conn:
        # Execute the SQL directly since it's an INSERT ... ON CONFLICT statement
        result = conn.execute(text(sql_content))
        conn.commit()
        
        print(f"KPI calculations completed. Rows affected: {result.rowcount}")
    
    print("KPI Calculations completed successfully!")

if __name__ == "__main__":
    run_kpi_calculations()