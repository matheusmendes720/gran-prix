#!/bin/bash
# Run Flask API Server
export FLASK_APP=demand_forecasting/api.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000

