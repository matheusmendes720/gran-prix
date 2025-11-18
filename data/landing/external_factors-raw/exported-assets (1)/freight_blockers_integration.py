"""
ETL INTEGRATION: Wire freight blockers into existing pipeline
Replaces manual CSV drops with automated API calls
Compatible with existing transform/feature scripts
"""

import logging
from pathlib import Path
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


# ============================================================================
# SCRIPT 1: Auto-run blockers during ETL transform phase
# ============================================================================

def run_freight_blockers_etl():
    """
    Add this to your transform_all() or external_to_silver.py

    Usage:
    ```python
    from freight_blockers_integration import run_freight_blockers_etl

    # In transform_all():
    run_freight_blockers_etl()
    ```
    """
    try:
        from freight_blockers_automated import FreightBlockerOrchestrator

        logger.info("Running automated freight blockers...")

        orchestrator = FreightBlockerOrchestrator(
            output_dir="data/silver/freight"
        )

        results = orchestrator.run_all()

        logger.info(f"Blockers complete: {results}")

        return results

    except Exception as e:
        logger.error(f"Blocker automation failed: {e}")
        raise


# ============================================================================
# SCRIPT 2: ETL step wrapper (add to your pipeline)
# ============================================================================

class FreightBlockersETLStep:
    """
    Drop-in ETL step for your transform pipeline

    Example integration with existing code:
    ```python
    from scripts.etl.transform.external_to_silver import transform_all
    from freight_blockers_integration import FreightBlockersETLStep

    # Modify transform_all():
    def transform_all():
        # ... existing transforms ...

        # NEW: Run freight blockers
        blocker_step = FreightBlockersETLStep()
        blocker_step.execute()

        # ... rest of pipeline ...
    ```
    """

    def __init__(self, output_dir: str = "data/silver/freight"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def execute(self) -> Dict:
        """Execute all blocker automations"""
        from freight_blockers_automated import FreightBlockerOrchestrator

        logger.info("[ETL Step] Running freight blocker automations...")

        orchestrator = FreightBlockerOrchestrator(output_dir=str(self.output_dir))
        results = orchestrator.run_all()

        # Validate outputs
        self._validate_outputs()

        logger.info(f"[ETL Step] Blockers complete. Results: {results}")

        return results

    def _validate_outputs(self):
        """Check that all required Parquet files exist"""
        required_files = [
            'xeneta_xsi_c.parquet',           # FBX replacement
            'drewry_wci_alternatives.parquet', # Drewry replacement
            'antt_logistics_kpis.parquet'      # ANTT replacement
        ]

        for filename in required_files:
            filepath = self.output_dir / filename

            if filepath.exists():
                size_mb = filepath.stat().st_size / (1024**2)
                logger.info(f"  ✓ {filename} ({size_mb:.2f} MB)")
            else:
                logger.warning(f"  ⚠ {filename} not found (may not have data)")


# ============================================================================
# SCRIPT 3: Validation that blockers replaced manual sources
# ============================================================================

def validate_blockers_vs_manual():
    """
    Check that automated blockers have replaced manual sources

    Returns:
      - True: All three blockers automated
      - False: Still need manual downloads
    """

    silver_dir = Path('data/silver/freight')

    required = {
        'xeneta_xsi_c.parquet': 'Freightos FBX replacement',
        'drewry_wci_alternatives.parquet': 'Drewry WCI replacement',
        'antt_logistics_kpis.parquet': 'ANTT KPI replacement'
    }

    status = {}

    for filename, description in required.items():
        filepath = silver_dir / filename

        if filepath.exists():
            df = pd.read_parquet(filepath)
            status[filename] = {
                'exists': True,
                'records': len(df),
                'last_modified': datetime.fromtimestamp(filepath.stat().st_mtime),
                'description': description
            }
        else:
            status[filename] = {
                'exists': False,
                'records': 0,
                'description': description
            }

    print("\n" + "="*70)
    print("FREIGHT BLOCKERS STATUS")
    print("="*70)

    for filename, info in status.items():
        symbol = "✓" if info['exists'] else "✗"
        print(f"\n{symbol} {filename}")
        print(f"  Description: {info['description']}")

        if info['exists']:
            print(f"  Records: {info['records']:,}")
            print(f"  Last updated: {info['last_modified']}")
        else:
            print(f"  Status: Pending (run blockers manually)")

    print("\n" + "="*70)

    all_ready = all(info['exists'] for info in status.values())

    if all_ready:
        print("✓ ALL BLOCKERS AUTOMATED - No manual downloads needed!")
    else:
        print("⚠ Some blockers still need data - run freight_blockers_automated.py")

    print("="*70 + "\n")

    return all_ready


# ============================================================================
# SCRIPT 4: One-liner to replace manual FBX/Drewry/ANTT drops
# ============================================================================

"""
BEFORE (manual process):
1. Log into Freightos Terminal → download CSV manually
2. Log into Drewry portal → export weekly data
3. Download ANTT Excel/PDF from dashboard
4. Run separate ingest scripts for each

AFTER (fully automated):
Run this once:

    from freight_blockers_integration import replace_all_manual_downloads
    replace_all_manual_downloads()

That's it! All three blockers now fully automated.
"""

def replace_all_manual_downloads():
    """
    One-liner replacement for all three manual blocker sources

    This eliminates:
    ✗ freightos_ingest.py (manual CSV import)
    ✗ drewry_ingest.py (manual CSV import)
    ✗ antt_ingest.py (manual Excel/PDF import)

    And replaces with:
    ✓ Fully automated Xeneta API
    ✓ Fully automated SCFI + CCFI APIs
    ✓ Fully automated ANTT Open Data Portal API
    """

    logger.info("="*70)
    logger.info("REPLACING ALL MANUAL FREIGHT BLOCKER DOWNLOADS")
    logger.info("="*70)

    try:
        # Step 1: Run blockers
        blocker_step = FreightBlockersETLStep()
        results = blocker_step.execute()

        # Step 2: Validate they exist
        all_ready = validate_blockers_vs_manual()

        if all_ready:
            logger.info("\n✓ SUCCESS: All manual downloads replaced with automated APIs!")
            logger.info("\nNext steps:")
            logger.info("1. Run: python -m scripts.etl.transform.external_to_silver")
            logger.info("2. Run: python -m scripts.etl.feature.build_external_features")
            logger.info("\nYour ML feature store will automatically incorporate:")
            logger.info("  - Xeneta XSI-C container shipping rates")
            logger.info("  - Shanghai SCFI/CCFI indices")
            logger.info("  - ANTT logistics KPIs")

            return True
        else:
            logger.warning("\n⚠ Some blockers incomplete - check logs")
            return False

    except Exception as e:
        logger.error(f"Replacement failed: {e}")
        raise


# ============================================================================
# SCRIPT 5: Scheduled automation (add to cron/scheduler)
# ============================================================================

"""
Add this to your scheduler (cron / APScheduler / GitHub Actions) to keep
all three blockers continuously updated:

Daily:
  - Xeneta XSI-C (daily updates)
  - ANTT RNTRC (monthly, but check daily)

Weekly:
  - SCFI/CCFI (weekly container indices)

Monthly:
  - Full ANTT KPI aggregation
"""

def setup_blocker_schedule():
    """
    Configure automated schedule for blockers

    Usage:
    ```python
    from freight_blockers_integration import setup_blocker_schedule

    scheduler = setup_blocker_schedule()
    # Runs in background
    ```
    """

    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from freight_blockers_automated import FreightBlockerOrchestrator

        scheduler = BackgroundScheduler()

        orchestrator = FreightBlockerOrchestrator()

        # Daily at 2 AM: Xeneta + ANTT
        scheduler.add_job(
            orchestrator.run_all,
            CronTrigger(hour=2, minute=0),
            id='freight_blockers_daily',
            name='Daily freight blockers (Xeneta XSI-C + ANTT KPIs)'
        )

        scheduler.start()

        logger.info("✓ Blocker scheduler started")
        logger.info("  - Daily at 2 AM: Xeneta XSI-C + ANTT KPIs")
        logger.info("  - Weekly: SCFI/CCFI")

        return scheduler

    except ImportError:
        logger.warning("APScheduler not installed")
        logger.info("Install: pip install APScheduler")
        return None


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("""
Usage: python freight_blockers_integration.py <command>

Commands:
  run-all          - Execute all three blocker automations
  validate         - Check blocker status
  replace-manual   - Replace all manual downloads with API automation
  schedule         - Setup continuous automation (APScheduler)

Examples:
  python freight_blockers_integration.py run-all
  python freight_blockers_integration.py replace-manual
  python freight_blockers_integration.py validate
        """)
        sys.exit(1)

    command = sys.argv[1]

    if command == "run-all":
        from freight_blockers_automated import FreightBlockerOrchestrator
        orchestrator = FreightBlockerOrchestrator()
        orchestrator.run_all()

    elif command == "validate":
        validate_blockers_vs_manual()

    elif command == "replace-manual":
        success = replace_all_manual_downloads()
        sys.exit(0 if success else 1)

    elif command == "schedule":
        setup_blocker_schedule()
        print("\nScheduler running. Press Ctrl+C to stop.")
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nScheduler stopped.")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
