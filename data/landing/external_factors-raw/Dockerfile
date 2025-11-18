FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
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
