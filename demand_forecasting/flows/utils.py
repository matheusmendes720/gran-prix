from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LANDING_ROOT = PROJECT_ROOT / "data" / "landing"
LOG_ROOT = PROJECT_ROOT / "logs" / "pipeline"


def ensure_directory(path: Path) -> Path:
    """Create the directory if it does not exist and return it."""

    path.mkdir(parents=True, exist_ok=True)
    return path


def landing_path(domain: str, layer: str, run_folder: str | None = None) -> Path:
    """Return the landing path for the given domain and layer."""

    base = ensure_directory(LANDING_ROOT / layer / domain)
    if run_folder:
        base = ensure_directory(base / run_folder)
    return base


def bronze_folder(domain: str, run_date: date, qualifier: str | None = None) -> Path:
    folder = run_date.strftime("%Y%m%d")
    if qualifier:
        folder = f"{folder}-{qualifier}"
    return landing_path(domain, "bronze", folder)


def silver_folder(domain: str, run_date: date) -> Path:
    folder = run_date.strftime("%Y%m%d")
    return landing_path(domain, "silver", folder)


def manifest_path(domain: str, run_date: date) -> Path:
    folder = run_date.strftime("%Y%m%d")
    return bronze_folder(domain, run_date) / f"manifest-{folder}.json"


def write_json(data: Any, path: Path) -> Path:
    ensure_directory(path.parent)
    with path.open("w", encoding="utf-8") as f:  # pragma: no cover - simple IO
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def write_manifest(domain: str, run_date: date, entries: Iterable[dict[str, Any]]) -> Path:
    payload = {
        "domain": domain,
        "run_date": run_date.isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "entries": list(entries),
    }
    path = manifest_path(domain, run_date)
    return write_json(payload, path)


def load_env(name: str, *, required: bool = False) -> str | None:
    value = os.getenv(name)
    if not value and required:
        raise RuntimeError(f"Environment variable '{name}' must be set for ingestion flow.")
    return value


@dataclass(slots=True)
class PersistedArtifact:
    domain: str
    layer: str
    path: Path
    record_count: int
    metadata: dict[str, Any]

    def to_manifest_entry(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "layer": self.layer,
            "path": str(self.path.relative_to(PROJECT_ROOT)),
            "record_count": self.record_count,
            "metadata": self.metadata,
        }

