# Freight Data Automation Makefile

.PHONY: help install download clean docker-build docker-run schedule test

help:
	@echo "Freight Data Automation Commands"
	@echo "================================"
	@echo "make install       - Install dependencies"
	@echo "make download      - Download freight data (one-time)"
	@echo "make schedule      - Start scheduled downloads"
	@echo "make docker-build  - Build Docker image"
	@echo "make docker-run    - Run in Docker container"
	@echo "make clean         - Clean up generated files"
	@echo "make test          - Run tests"
	@echo "make example       - Run example notebook"

install:
	pip install -r requirements.txt
	mkdir -p data/manual

download:
	python -c "from freight_data_automation import FreightAutomationOrchestrator; orchestrator = FreightAutomationOrchestrator(); orchestrator.download_all(); orchestrator.print_status()"

schedule:
	python -c "from freight_data_scheduler import FreightDataScheduler; scheduler = FreightDataScheduler(); scheduler.setup_daily_schedule(); scheduler.run_continuous()"

docker-build:
	docker build -t freight-data-automation:latest .

docker-run:
	docker run --rm -v $$(pwd)/data:/app/data freight-data-automation:latest

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

clean:
	rm -rf data/manual/*.csv
	rm -rf __pycache__
	rm -rf *.pyc
	find . -type d -name __pycache__ -delete

test:
	python -m pytest tests/ -v

example:
	python example_notebook.py

status:
	@echo "Files in data/manual:"
	@ls -lh data/manual/ 2>/dev/null || echo "No data directory yet"

logs:
	docker logs -f freight-fetcher-scheduled 2>/dev/null || echo "Container not running"

update:
	git pull
	pip install -r requirements.txt

.PHONY: help install download clean docker-build docker-run schedule test
