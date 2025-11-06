#!/usr/bin/env python3
"""
Quick validation script to verify the PostgreSQL refactoring
Checks migrations, API routes, and frontend components
"""
import sys
import os
from pathlib import Path

backend_dir = Path(__file__).parent
project_root = backend_dir.parent

def check_file(file_path, description):
    """Check if a file exists"""
    full_path = project_root / file_path
    exists = full_path.exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {file_path}")
    return exists

def check_content(file_path, search_text, description):
    """Check if file contains specific content"""
    full_path = project_root / file_path
    if not full_path.exists():
        print(f"❌ {description}: File not found")
        return False
    
    content = full_path.read_text(encoding='utf-8')
    exists = search_text in content
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    return exists

def main():
    print("=" * 70)
    print("Nova Corrente - PostgreSQL Refactoring Validation")
    print("=" * 70)
    print()
    
    all_checks_passed = True
    
    # Backend Files
    print("📦 Backend Files:")
    print("-" * 70)
    all_checks_passed &= check_file("backend/alembic/versions/001_initial_postgres_schema.py", "Alembic migration")
    all_checks_passed &= check_file("backend/api/enhanced_api.py", "Flask API (main)")
    all_checks_passed &= check_file("backend/api/v1/routes.py", "API v1 routes")
    all_checks_passed &= check_file("backend/scripts/generate_demo_data.py", "Demo data generator")
    all_checks_passed &= check_file("backend/scripts/setup_database.py", "Database setup script")
    all_checks_passed &= check_file("backend/run_flask_api.py", "Flask API runner")
    all_checks_passed &= check_file("backend/Dockerfile", "Backend Dockerfile")
    all_checks_passed &= check_file("backend/docker-entrypoint.sh", "Docker entrypoint")
    all_checks_passed &= check_file("backend/requirements_deployment.txt", "Deployment requirements")
    print()
    
    # Frontend Files
    print("🎨 Frontend Files:")
    print("-" * 70)
    all_checks_passed &= check_file("frontend/src/lib/api-client.ts", "API client")
    all_checks_passed &= check_file("frontend/src/hooks/use-api.ts", "SWR hooks")
    all_checks_passed &= check_file("frontend/src/components/KPIDashboard.tsx", "KPI Dashboard")
    all_checks_passed &= check_file("frontend/src/components/MaterialsTable.tsx", "Materials Table")
    all_checks_passed &= check_file("frontend/src/components/DemandChart.tsx", "Demand Chart")
    all_checks_passed &= check_file("frontend/src/app/page.tsx", "Main dashboard page")
    all_checks_passed &= check_file("frontend/package.json", "Frontend package.json")
    print()
    
    # Migration Content Checks
    print("🗄️  Database Migration Content:")
    print("-" * 70)
    all_checks_passed &= check_content(
        "backend/alembic/versions/001_initial_postgres_schema.py",
        "CREATE SCHEMA IF NOT EXISTS core",
        "Creates core schema"
    )
    all_checks_passed &= check_content(
        "backend/alembic/versions/001_initial_postgres_schema.py",
        "CREATE TABLE core.dim_calendar",
        "Creates calendar dimension"
    )
    all_checks_passed &= check_content(
        "backend/alembic/versions/001_initial_postgres_schema.py",
        "PARTITION BY RANGE (full_date)",
        "Creates partitioned fact tables"
    )
    all_checks_passed &= check_content(
        "backend/alembic/versions/001_initial_postgres_schema.py",
        "CREATE TABLE analytics.forecasts",
        "Creates forecasts table"
    )
    print()
    
    # API Routes Content Checks
    print("🔌 API Routes Content:")
    print("-" * 70)
    all_checks_passed &= check_content(
        "backend/api/v1/routes.py",
        "@api_v1.route('/items', methods=['GET'])",
        "Items endpoint"
    )
    all_checks_passed &= check_content(
        "backend/api/v1/routes.py",
        "@api_v1.route('/analytics/kpis', methods=['GET'])",
        "KPIs endpoint"
    )
    all_checks_passed &= check_content(
        "backend/api/v1/routes.py",
        "@api_v1.route('/forecasts', methods=['GET'])",
        "Forecasts endpoint"
    )
    all_checks_passed &= check_content(
        "backend/api/v1/routes.py",
        "@api_v1.route('/recommendations', methods=['GET'])",
        "Recommendations endpoint"
    )
    all_checks_passed &= check_content(
        "backend/api/v1/routes.py",
        "@api_v1.route('/alerts', methods=['GET'])",
        "Alerts endpoint"
    )
    print()
    
    # Frontend Components Content Checks
    print("⚛️  Frontend Components Content:")
    print("-" * 70)
    all_checks_passed &= check_content(
        "frontend/src/lib/api-client.ts",
        "class NovaCorrenteAPI",
        "API client class"
    )
    all_checks_passed &= check_content(
        "frontend/src/hooks/use-api.ts",
        "export function useKPIs",
        "useKPIs hook"
    )
    all_checks_passed &= check_content(
        "frontend/src/components/KPIDashboard.tsx",
        "export function KPIDashboard",
        "KPIDashboard component"
    )
    all_checks_passed &= check_content(
        "frontend/src/components/MaterialsTable.tsx",
        "export function MaterialsTable",
        "MaterialsTable component"
    )
    all_checks_passed &= check_content(
        "frontend/src/components/DemandChart.tsx",
        "export function DemandChart",
        "DemandChart component"
    )
    print()
    
    # Setup Files
    print("🚀 Setup & Deployment Files:")
    print("-" * 70)
    all_checks_passed &= check_file("SETUP_AND_RUN.bat", "Windows setup script")
    all_checks_passed &= check_file("SETUP_GUIDE.md", "Setup documentation")
    all_checks_passed &= check_file("docker-compose.yml", "Docker Compose config")
    print()
    
    # File Statistics
    print("📊 File Statistics:")
    print("-" * 70)
    
    migration_file = project_root / "backend/alembic/versions/001_initial_postgres_schema.py"
    if migration_file.exists():
        lines = len(migration_file.read_text(encoding='utf-8').splitlines())
        print(f"   Migration file: {lines} lines")
    
    routes_file = project_root / "backend/api/v1/routes.py"
    if routes_file.exists():
        lines = len(routes_file.read_text(encoding='utf-8').splitlines())
        print(f"   API routes: {lines} lines")
    
    demo_data_file = project_root / "backend/scripts/generate_demo_data.py"
    if demo_data_file.exists():
        lines = len(demo_data_file.read_text(encoding='utf-8').splitlines())
        print(f"   Demo data generator: {lines} lines")
    
    api_client_file = project_root / "frontend/src/lib/api-client.ts"
    if api_client_file.exists():
        lines = len(api_client_file.read_text(encoding='utf-8').splitlines())
        print(f"   Frontend API client: {lines} lines")
    
    print()
    
    # Summary
    print("=" * 70)
    if all_checks_passed:
        print("✅ All validation checks PASSED!")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r backend/requirements_deployment.txt")
        print("2. Start PostgreSQL on localhost:5432")
        print("3. Run setup: python backend/scripts/setup_database.py")
        print("4. Start API: python backend/run_flask_api.py")
        print("5. Start frontend: cd frontend && npm install && npm run dev")
        print()
        print("Or use Docker: docker-compose up --build")
        return 0
    else:
        print("❌ Some validation checks FAILED")
        print("Please review the output above for missing files or content")
        return 1

if __name__ == '__main__':
    sys.exit(main())
