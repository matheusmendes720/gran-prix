
# Create Docker setup files

dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    wget \\
    curl \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY freight_data_automation.py .
COPY trading_econ_fetcher.py .
COPY worldbank_freight_fetcher.py .
COPY selenium_freight_scraper.py .
COPY freight_data_scheduler.py .
COPY freight_config.py .

# Create data directory
RUN mkdir -p /app/data/manual

# Environment variables
ENV TRADING_ECONOMICS_API_KEY="guest:guest"
ENV FREIGHT_DATA_DIR="/app/data/manual"
ENV FREIGHT_LOG_LEVEL="INFO"

# Default command: one-time run
CMD ["python", "-c", "from freight_data_automation import FreightAutomationOrchestrator; orchestrator = FreightAutomationOrchestrator(); orchestrator.download_all(); orchestrator.print_status()"]
'''

with open('Dockerfile', 'w') as f:
    f.write(dockerfile_content)

print("✓ Dockerfile created")

# Docker compose for scheduling
compose_content = '''version: '3.8'

services:
  freight-fetcher:
    build: .
    container_name: freight-data-fetcher
    environment:
      - TRADING_ECONOMICS_API_KEY=guest:guest
      - FREIGHT_DATA_DIR=/app/data/manual
      - FREIGHT_LOG_LEVEL=INFO
      - TZ=America/Sao_Paulo
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    # Run every day at 2 AM (cron-like scheduling)
    restart: unless-stopped
    command: |
      python -c "
      from freight_data_scheduler import FreightDataScheduler
      import time
      scheduler = FreightDataScheduler()
      scheduler.setup_daily_schedule()
      scheduler.run_continuous()
      "

  # Optional: Selenium standalone for SCFI scraping
  selenium:
    image: selenium/standalone-chrome:latest
    container_name: freight-selenium
    ports:
      - "4444:4444"
      - "7900:7900"
    volumes:
      - /dev/shm:/dev/shm
    environment:
      - SE_NODE_MAX_SESSIONS=2
      - SE_NODE_SESSION_TIMEOUT=300
    profiles:
      - scfi-scraping
'''

with open('docker-compose.yml', 'w') as f:
    f.write(compose_content)

print("✓ docker-compose.yml created")

# Requirements file
requirements = '''requests>=2.31.0
beautifulsoup4>=4.12.0
tradingeconomics>=0.0.42
selenium>=4.15.0
webdriver-manager>=4.0.0
pandas>=2.1.0
openpyxl>=3.1.0
schedule>=1.2.0
APScheduler>=3.10.4
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements)

print("✓ requirements.txt created")

# Docker build & run script
docker_run_script = '''#!/bin/bash

# Freight Data Automation Docker Helper

set -e

case "$1" in
  build)
    echo "Building Docker image..."
    docker build -t freight-data-automation:latest .
    ;;
  
  run-once)
    echo "Running one-time data fetch..."
    docker run --rm \\
      -v $(pwd)/data:/app/data \\
      -e TRADING_ECONOMICS_API_KEY="${TRADING_ECONOMICS_API_KEY:-guest:guest}" \\
      freight-data-automation:latest
    ;;
  
  run-scheduled)
    echo "Running scheduled fetcher (continuous)..."
    docker run -d \\
      --name freight-fetcher-scheduled \\
      -v $(pwd)/data:/app/data \\
      -e TRADING_ECONOMICS_API_KEY="${TRADING_ECONOMICS_API_KEY:-guest:guest}" \\
      freight-data-automation:latest \\
      python freight_data_scheduler.py --mode schedule
    ;;
  
  compose-up)
    echo "Starting with Docker Compose..."
    docker-compose up -d
    ;;
  
  compose-down)
    echo "Stopping Docker Compose services..."
    docker-compose down
    ;;
  
  logs)
    echo "Following logs..."
    docker logs -f freight-fetcher-scheduled
    ;;
  
  shell)
    echo "Opening shell in container..."
    docker run -it --rm \\
      -v $(pwd)/data:/app/data \\
      freight-data-automation:latest \\
      /bin/bash
    ;;
  
  *)
    echo "Freight Data Automation Docker Helper"
    echo ""
    echo "Usage: $0 {build|run-once|run-scheduled|compose-up|compose-down|logs|shell}"
    echo ""
    echo "Commands:"
    echo "  build           - Build Docker image"
    echo "  run-once        - Run one-time fetch"
    echo "  run-scheduled   - Run with scheduling (background)"
    echo "  compose-up      - Start with Docker Compose"
    echo "  compose-down    - Stop Docker Compose services"
    echo "  logs            - Follow logs of running container"
    echo "  shell           - Open bash shell in container"
    echo ""
    echo "Environment variables:"
    echo "  TRADING_ECONOMICS_API_KEY - Trading Economics API key (default: guest:guest)"
    exit 1
    ;;
esac
'''

with open('docker-run.sh', 'w') as f:
    f.write(docker_run_script)

import os
os.chmod('docker-run.sh', 0o755)

print("✓ docker-run.sh created (executable)")

# GitHub Actions workflow
github_action = '''name: Fetch Freight Data

on:
  schedule:
    # Daily at 2 AM UTC
    - cron: '0 2 * * *'
  workflow_dispatch:

jobs:
  fetch-data:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Fetch freight data
      env:
        TRADING_ECONOMICS_API_KEY: ${{ secrets.TRADING_ECONOMICS_API_KEY }}
      run: |
        python -c "
        from freight_data_automation import FreightAutomationOrchestrator
        orchestrator = FreightAutomationOrchestrator()
        orchestrator.download_all()
        orchestrator.print_status()
        "
    
    - name: Upload data artifacts
      if: success()
      uses: actions/upload-artifact@v3
      with:
        name: freight-data-${{ github.run_id }}
        path: data/manual/*.csv
        retention-days: 90
    
    - name: Commit and push updates
      if: success()
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add data/manual/
        git commit -m "chore: update freight data $(date -u +'%Y-%m-%d')" || echo "No changes to commit"
        git push
'''

os.makedirs('.github/workflows', exist_ok=True)
with open('.github/workflows/fetch-freight-data.yml', 'w') as f:
    f.write(github_action)

print("✓ .github/workflows/fetch-freight-data.yml created")

# K8s manifest
k8s_manifest = '''apiVersion: batch/v1
kind: CronJob
metadata:
  name: freight-data-fetcher
  namespace: default
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM UTC
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: fetcher
            image: freight-data-automation:latest
            imagePullPolicy: IfNotPresent
            env:
            - name: TRADING_ECONOMICS_API_KEY
              valueFrom:
                secretKeyRef:
                  name: freight-secrets
                  key: trading-economics-key
            - name: FREIGHT_DATA_DIR
              value: /data
            volumeMounts:
            - name: data
              mountPath: /data
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "512Mi"
                cpu: "500m"
          volumes:
          - name: data
            persistentVolumeClaim:
              claimName: freight-data-pvc
          restartPolicy: OnFailure
---
apiVersion: v1
kind: Secret
metadata:
  name: freight-secrets
type: Opaque
stringData:
  trading-economics-key: "guest:guest"  # Change to actual key
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: freight-data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
'''

os.makedirs('k8s', exist_ok=True)
with open('k8s/freight-cronjob.yaml', 'w') as f:
    f.write(k8s_manifest)

print("✓ k8s/freight-cronjob.yaml created")

print("\n" + "="*60)
print("CONTAINER & DEPLOYMENT FILES CREATED")
print("="*60)
print("\nFiles for containerization:")
print("- Dockerfile                    - Docker image definition")
print("- docker-compose.yml            - Multi-container setup")
print("- docker-run.sh                 - Helper script")
print("- requirements.txt              - Python dependencies")
print("\nFiles for CI/CD:")
print("- .github/workflows/fetch-freight-data.yml  - GitHub Actions")
print("- k8s/freight-cronjob.yaml      - Kubernetes CronJob")
print("\n" + "="*60)
