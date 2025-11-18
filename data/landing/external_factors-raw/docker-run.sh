#!/bin/bash

# Freight Data Automation Docker Helper

set -e

case "$1" in
  build)
    echo "Building Docker image..."
    docker build -t freight-data-automation:latest .
    ;;

  run-once)
    echo "Running one-time data fetch..."
    docker run --rm \
      -v $(pwd)/data:/app/data \
      -e TRADING_ECONOMICS_API_KEY="${TRADING_ECONOMICS_API_KEY:-guest:guest}" \
      freight-data-automation:latest
    ;;

  run-scheduled)
    echo "Running scheduled fetcher (continuous)..."
    docker run -d \
      --name freight-fetcher-scheduled \
      -v $(pwd)/data:/app/data \
      -e TRADING_ECONOMICS_API_KEY="${TRADING_ECONOMICS_API_KEY:-guest:guest}" \
      freight-data-automation:latest \
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
    docker run -it --rm \
      -v $(pwd)/data:/app/data \
      freight-data-automation:latest \
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
