#!/bin/bash
set -e

echo "============================================================"
echo "Nova Corrente Backend - Docker Entrypoint"
echo "============================================================"

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
python scripts/setup_database.py

# Start the application
echo "Starting Flask API server..."
exec gunicorn -b 0.0.0.0:5000 --workers 4 --timeout 120 backend.api.enhanced_api:app
