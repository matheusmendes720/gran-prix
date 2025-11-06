#!/usr/bin/env python3
"""
Database setup script for Nova Corrente PostgreSQL
Runs Alembic migrations and generates demo data
"""
import sys
import os
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent.parent
project_root = backend_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import subprocess
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment
load_dotenv(backend_dir / '.env')

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://nova_corrente:password@localhost:5432/nova_corrente')

def wait_for_db(max_retries=30, retry_interval=2):
    """Wait for PostgreSQL to be ready"""
    print("⏳ Waiting for PostgreSQL to be ready...")
    
    engine = None
    for i in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                conn.execute(text('SELECT 1'))
                print("✅ PostgreSQL is ready!")
                engine.dispose()
                return True
        except Exception as e:
            if i == 0:
                print(f"   Database not ready yet, retrying...")
            time.sleep(retry_interval)
    
    print("❌ Failed to connect to PostgreSQL after maximum retries")
    return False

def run_migrations():
    """Run Alembic migrations"""
    print("\n📦 Running database migrations...")
    
    try:
        # Change to backend directory for alembic
        os.chdir(backend_dir)
        
        # Run alembic upgrade
        result = subprocess.run(
            ['alembic', 'upgrade', 'head'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Migrations completed successfully!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Migration failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False

def generate_demo_data():
    """Generate demo data"""
    print("\n📊 Generating demo data...")
    
    try:
        # Run the demo data generator
        result = subprocess.run(
            [sys.executable, 'scripts/generate_demo_data.py'],
            capture_output=True,
            text=True,
            cwd=backend_dir
        )
        
        if result.returncode == 0:
            print("✅ Demo data generated successfully!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Demo data generation failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error generating demo data: {e}")
        return False

def verify_setup():
    """Verify database setup"""
    print("\n🔍 Verifying database setup...")
    
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Check schemas
            schemas = conn.execute(text("""
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name IN ('core', 'analytics', 'support', 'staging')
                ORDER BY schema_name
            """)).fetchall()
            
            print(f"   Found {len(schemas)} schemas: {[s[0] for s in schemas]}")
            
            # Check tables
            tables = conn.execute(text("""
                SELECT table_schema, table_name 
                FROM information_schema.tables 
                WHERE table_schema IN ('core', 'analytics', 'support', 'staging')
                ORDER BY table_schema, table_name
            """)).fetchall()
            
            print(f"   Found {len(tables)} tables")
            
            # Check data counts
            item_count = conn.execute(text("SELECT COUNT(*) FROM core.dim_item")).scalar()
            demand_count = conn.execute(text("SELECT COUNT(*) FROM core.fact_demand_daily")).scalar()
            
            print(f"   Items: {item_count}")
            print(f"   Demand records: {demand_count}")
            
            if item_count > 0 and demand_count > 0:
                print("✅ Database verification successful!")
                return True
            else:
                print("⚠️ Database is set up but may be missing data")
                return False
                
        engine.dispose()
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("Nova Corrente Database Setup")
    print("=" * 60)
    print(f"Database URL: {DATABASE_URL.replace(DATABASE_URL.split('@')[0].split('//')[1], '***')}")
    print("=" * 60)
    
    # Step 1: Wait for database
    if not wait_for_db():
        print("\n❌ Setup failed: Could not connect to database")
        sys.exit(1)
    
    # Step 2: Run migrations
    if not run_migrations():
        print("\n❌ Setup failed: Migration error")
        sys.exit(1)
    
    # Step 3: Generate demo data
    if not generate_demo_data():
        print("\n⚠️ Warning: Demo data generation failed (continuing anyway)")
    
    # Step 4: Verify setup
    if not verify_setup():
        print("\n⚠️ Warning: Verification found issues")
    
    print("\n" + "=" * 60)
    print("✅ Database setup complete!")
    print("=" * 60)
    print("\n🚀 You can now start the API server with:")
    print("   python -m gunicorn -b 0.0.0.0:5000 -w 4 backend.api.enhanced_api:app")
    print("   or: docker-compose up")
    print()

if __name__ == '__main__':
    main()
