#!/usr/bin/env python3
"""Utility to orchestrate timeout isolation test runs.

Runs pytest, k6 smoke test, and locust headless load. Gracefully skips
optional tools when binaries are unavailable and records structured
output under reports/raw/.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = BASE_DIR / "reports"
RAW_DIR = REPORTS_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

SUITE_TARGETS = {
    "pytest": {
        "binary": "pytest",
        "args": ["-q", "--maxfail=1"],
        "output_file": RAW_DIR / "pytest_output.txt",
    },
    "k6": {
        "binary": "k6",
        "args": ["run", "tools/k6/bacen_timeout_smoke.js"],
        "output_file": RAW_DIR / "k6_output.txt",
    },
    "locust": {
        "binary": "locust",
        "args": [
            "-f",
            "tools/locust/locustfile.py",
            "--headless",
            "-u",
            "20",
            "-r",
            "5",
            "-t",
            "1m",
        ],
        "output_file": RAW_DIR / "locust_output.txt",
    },
}


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_command(name: str, binary: str, args: List[str], output_file: Path) -> dict:
    result: dict = {
        "name": name,
        "timestamp": _timestamp(),
        "command": " ".join([binary, *args]),
        "status": "skipped",
        "returncode": None,
        "message": "",
        "output_file": str(output_file.relative_to(BASE_DIR)),
    }

    if shutil.which(binary) is None:
        result["message"] = f"{binary} not available on PATH"
        return result

    try:
        completed = subprocess.run(
            [binary, *args],
            cwd=str(BASE_DIR),
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:  # pragma: no cover - defensive
        result["message"] = str(exc)
        return result

    output_file.write_text(
        f"# {result['command']}\n"
        f"# timestamp: {result['timestamp']}\n\n"
        f"{completed.stdout}\n"
        f"--- stderr ---\n{completed.stderr}\n"
    )

    result["returncode"] = completed.returncode
    if completed.returncode == 0:
        result["status"] = "passed"
        result["message"] = "completed successfully"
    else:
        result["status"] = "failed"
        trimmed = completed.stderr.strip() or completed.stdout.strip()
        result["message"] = trimmed.splitlines()[0] if trimmed else "exit code != 0"

    return result


def main(selected: Optional[List[str]] = None) -> int:
    targets = selected or list(SUITE_TARGETS.keys())
    summary: List[dict] = []

    for name in targets:
        target = SUITE_TARGETS.get(name)
        if not target:
            summary.append(
                {
                    "name": name,
                    "timestamp": _timestamp(),
                    "status": "skipped",
                    "message": "unknown target",
                }
            )
            continue

        result = _run_command(
            name,
            binary=target["binary"],
            args=target["args"],
            output_file=target["output_file"],
        )
        summary.append(result)
        print(f"[{result['status']}] {name}: {result['message']}")

    summary_file = RAW_DIR / f"run_suite_summary_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"Summary saved to {summary_file.relative_to(BASE_DIR)}")

    # Return non-zero if any required target failed
    failures = [s for s in summary if s.get("status") == "failed"]
    return 1 if failures else 0


if __name__ == "__main__":
    exit_code = main(sys.argv[1:] or None)
    sys.exit(exit_code)
