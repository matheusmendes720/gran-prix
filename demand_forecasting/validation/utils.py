"""Utilities for validation logging."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from demand_forecasting.flows.utils import LOG_ROOT, ensure_directory


VALIDATION_LOG_DIR = ensure_directory(LOG_ROOT / "validation")


def write_validation_result(name: str, payload: Mapping[str, Any]) -> Path:
    """Persist validation output as JSON with timestamped filename."""

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = VALIDATION_LOG_DIR / f"{timestamp}-{name}.json"
    with path.open("w", encoding="utf-8") as fh:  # pragma: no cover - simple IO
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    return path

