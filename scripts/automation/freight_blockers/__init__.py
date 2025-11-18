"""
Freight blockers automation package.

Contains utilities to replace manual freight data downloads with automated
fetchers. See `scripts/automation/freight_blockers/automated.py` for the
orchestrator and `integration.py` for ETL wiring helpers.
"""

__all__ = [
    "FreightBlockerOrchestrator",
    "FreightBlockersETLStep",
    "run_freight_blockers_etl",
    "replace_all_manual_downloads",
    "setup_blocker_schedule",
    "validate_blockers_vs_manual",
]

from .automated import FreightBlockerOrchestrator  # noqa: E402
from .integration import (  # noqa: E402
    FreightBlockersETLStep,
    replace_all_manual_downloads,
    run_freight_blockers_etl,
    setup_blocker_schedule,
    validate_blockers_vs_manual,
)

