#!/usr/bin/env python3
"""
Main entry point for Nova Corrente Demand Forecasting Pipeline
Run this script from the project root directory.
"""

import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the pipeline
from src.pipeline.run_pipeline import main

if __name__ == "__main__":
    main()
