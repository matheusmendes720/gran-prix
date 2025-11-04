# Backend Dockerfile - ML Processing Environment (Separate from Deployment)
# Nova Corrente - ML Processing Only
# 
# This Dockerfile is for ML PROCESSING ENVIRONMENT ONLY.
# NOT for deployment - ML processing runs in separate environment.
# 
# ML processing outputs results as Parquet to shared storage.
# Deployment reads these results (read-only access).

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy ML requirements (includes ML dependencies)
COPY backend/requirements_ml.txt ./requirements_ml.txt

# Install Python dependencies (including ML)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_ml.txt

# Copy application code (ML processing code)
COPY backend/ ./backend/
COPY shared/ ./shared/

# Create necessary directories
RUN mkdir -p data models reports logs exports/ml_results

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV ML_RESULTS_PATH=/app/exports/ml_results

# Expose port (if ML API needed - optional)
EXPOSE 5001

# Default command (ML processing script)
CMD ["python", "-m", "backend.scripts.train_models_nova_corrente"]

