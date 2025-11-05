import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_RAW = BASE_DIR / "reports" / "raw"
REPORTS_RAW.mkdir(parents=True, exist_ok=True)


@pytest.fixture(params=[30, 10, 5, 1, None], ids=["timeout_30", "timeout_10", "timeout_5", "timeout_1", "timeout_default"])
def timeout(request):
    """Timeout values to test. None means use requests default."""
    return request.param


@pytest.fixture(params=[1, 3], ids=["retries_1", "retries_3"])
def max_retries(request):
    return request.param


@pytest.fixture(scope="session")
def run_live():
    """Whether to run live integration tests against real APIs."""
    return os.getenv("RUN_LIVE", "0") == "1"


@pytest.fixture
def trace_writer():
    """Utility to log test traces under reports/raw."""

    def _write(endpoint_name: str, variation: dict, metrics: dict):
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        entry = {
            "timestamp": timestamp,
            "endpoint": endpoint_name,
            "variation": variation,
            "metrics": metrics,
        }
        file_path = REPORTS_RAW / f"{endpoint_name}_traces.jsonl"
        with file_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return _write


@pytest.fixture(scope="session")
def bacen_base():
    return "https://api.bcb.gov.br/dados/serie/bcdata.sgs."


@pytest.fixture(scope="session")
def bacen_series_codes():
    return {"ipca": 433, "selic": 11, "exchange_rate": 1, "gdp": 4380}


@pytest.fixture(scope="session")
def openweather_base():
    return "https://api.openweathermap.org/data/2.5/weather"


@pytest.fixture(scope="session")
def healthcheck_url():
    return os.getenv("HEALTHCHECK_URL", "http://localhost:8000/api/v1/health")
