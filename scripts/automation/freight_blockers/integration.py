"""
ETL integration helpers for freight blocker automation.
"""

from __future__ import annotations

import logging
from datetime import datetime
import time
from pathlib import Path
from typing import Dict

import pandas as pd

from .automated import FreightBlockerOrchestrator

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------


def run_freight_blockers_etl(output_dir: str = "data/silver/freight") -> Dict[str, str]:
    """
    Execute the full blocker automation.

    Typical usage inside ``transform_all``:

    ```python
    from scripts.automation.freight_blockers.integration import run_freight_blockers_etl

    def transform_all():
        # … existing transforms …
        run_freight_blockers_etl()
    ```
    """

    logger.info("Running freight blocker automation (output=%s)…", output_dir)
    orchestrator = FreightBlockerOrchestrator(output_dir=output_dir)
    results = orchestrator.run_all()
    logger.info("Freight blockers completed: %s", results)
    return results


class FreightBlockersETLStep:
    """Drop-in ETL step wrapper."""

    REQUIRED_FILES = {
        "xeneta_xsi_c.parquet": "Freightos FBX replacement",
        "drewry_wci_alternatives.parquet": "Drewry WCI replacement",
        "antt_logistics_kpis.parquet": "ANTT KPI replacement",
    }

    def __init__(self, output_dir: str = "data/silver/freight") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def execute(self) -> Dict[str, str]:
        logger.info("[FreightBlockersETLStep] Starting execution.")
        orchestrator = FreightBlockerOrchestrator(output_dir=str(self.output_dir))
        results = orchestrator.run_all()
        self._validate_outputs()
        problematic = {name: status for name, status in results.items() if not str(status).startswith("OK")}
        if problematic:
            logger.warning("[FreightBlockersETLStep] Issues detected in freight blockers: %s", problematic)
        else:
            logger.info("[FreightBlockersETLStep] All blockers completed successfully.")
        return results

    def _validate_outputs(self) -> None:
        for filename, description in self.REQUIRED_FILES.items():
            filepath = self.output_dir / filename
            if filepath.exists():
                df = pd.read_parquet(filepath)
                logger.info(
                    "  OK - %s (%s rows) -> %s",
                    filename,
                    len(df),
                    description,
                )
            else:
                logger.warning(
                    "  WARN - %s missing -> automation may require attention (%s)",
                    filename,
                    description,
                )


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def validate_blockers_vs_manual(output_dir: str = "data/silver/freight") -> bool:
    """Print a status table confirming which blockers have produced data."""
    output = Path(output_dir)
    status = {}
    for filename, description in FreightBlockersETLStep.REQUIRED_FILES.items():
        filepath = output / filename
        if filepath.exists():
            df = pd.read_parquet(filepath)
            status[filename] = {
                "exists": True,
                "records": len(df),
                "last_modified": datetime.fromtimestamp(filepath.stat().st_mtime),
                "description": description,
            }
        else:
            status[filename] = {
                "exists": False,
                "records": 0,
                "description": description,
            }

    print("\n" + "=" * 70)
    print("FREIGHT BLOCKER STATUS")
    print("=" * 70)
    for filename, info in status.items():
        symbol = "✓" if info["exists"] else "✗"
        print(f"{symbol} {filename}")
        print(f"    Description : {info['description']}")
        if info["exists"]:
            print(f"    Records     : {info['records']:,}")
            print(f"    Last update : {info['last_modified']}")
        else:
            print("    Status      : Pending (run automation)")
        print()
    all_ready = all(info["exists"] for info in status.values())
    print("=" * 70)
    if all_ready:
        print("✓ All blockers automated – manual downloads no longer required.")
    else:
        print("⚠ Missing datasets – review automation logs.")
    print("=" * 70 + "\n")
    return all_ready


def replace_all_manual_downloads() -> bool:
    """
    Convenience one-liner to run blockers and confirm outputs exist.

    ```python
    from scripts.automation.freight_blockers.integration import replace_all_manual_downloads
    replace_all_manual_downloads()
    ```
    """

    step = FreightBlockersETLStep()
    step.execute()
    return validate_blockers_vs_manual(output_dir=str(step.output_dir))


# ---------------------------------------------------------------------------
# Scheduling
# ---------------------------------------------------------------------------


def setup_blocker_schedule() -> None:
    """Example APScheduler integration for ongoing automation."""
    try:
        from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore[import]
        from apscheduler.triggers.cron import CronTrigger  # type: ignore[import]
    except ImportError:
        logger.warning("APScheduler not installed. Install with `pip install apscheduler`.")
        return

    orchestrator = FreightBlockerOrchestrator()
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        orchestrator.run_all,
        CronTrigger(hour=2, minute=0),
        id="freight_blockers_daily",
        name="Daily freight blocker automation",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Freight blocker scheduler started (daily at 02:00).")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            """
Usage: python -m scripts.automation.freight_blockers.integration <command>

Commands:
  run-all          Execute blockers once
  validate         Check blocker outputs
  replace-manual   Run blockers and confirm manual downloads replaced
  schedule         Start APScheduler background cron
"""
        )
        raise SystemExit(1)

    command = sys.argv[1]
    if command == "run-all":
        run_freight_blockers_etl()
    elif command == "validate":
        validate_blockers_vs_manual()
    elif command == "replace-manual":
        success = replace_all_manual_downloads()
        raise SystemExit(0 if success else 1)
    elif command == "schedule":
        setup_blocker_schedule()
        try:
            while True:
                time.sleep(1)  # type: ignore[name-defined]
        except KeyboardInterrupt:  # pragma: no cover - CLI convenience
            print("\nScheduler stopped.")
    else:
        print(f"Unknown command: {command}")
        raise SystemExit(1)

