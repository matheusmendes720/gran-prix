from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Dict

from prefect import flow, get_run_logger, task

from demand_forecasting.features import FeatureBuilder
from demand_forecasting.flows import (
    climate_ingestion_flow,
    economic_ingestion_flow,
    regulatory_ingestion_flow,
)
from demand_forecasting.flows.utils import LOG_ROOT
from demand_forecasting.pipelines.training import ForecastingPipeline
from demand_forecasting.warehouse import WarehouseBuilder


RUN_LOG_PATH = LOG_ROOT / "runs.csv"


def _append_run_log(row: Dict[str, str]) -> None:
    RUN_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = RUN_LOG_PATH.exists()
    with RUN_LOG_PATH.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


@task
def build_warehouse_snapshot() -> Path:
    builder = WarehouseBuilder()
    return builder.run()


@task
def export_features(snapshot_path: Path) -> Path:
    builder = FeatureBuilder(snapshot_path=snapshot_path)
    return builder.export_features()


@task
def run_training(snapshot_path: Path) -> Dict[str, str]:
    builder = FeatureBuilder(snapshot_path=snapshot_path)
    pipeline = ForecastingPipeline(builder)
    artifacts = pipeline.run()
    summary = {
        "series_modeled": len(artifacts.forecasts),
        "alerts": sum(1 for v in artifacts.prescriptive.values() if v["stock_status"] == "critical"),
    }
    summary.update({k: str(v) for k, v in artifacts.metrics.items()})
    return summary


@task
def log_pipeline_run(status: str, snapshot_path: Path, metrics: Dict[str, int]) -> None:
    timestamp = datetime.utcnow().isoformat()
    row = {
        "timestamp": timestamp,
        "status": status,
        "snapshot_path": str(snapshot_path),
        "series_modeled": str(metrics.get("series_modeled", 0)),
        "critical_alerts": str(metrics.get("alerts", 0)),
        "metrics_summary": metrics.get("summary_path", ""),
    }
    _append_run_log(row)


@flow(name="nova-corrente-batch-cycle")
def batch_cycle_flow() -> Dict[str, str]:
    logger = get_run_logger()
    try:
        climate_paths = climate_ingestion_flow()
        economic_paths = economic_ingestion_flow()
        regulatory_paths = regulatory_ingestion_flow()
        snapshot_path = build_warehouse_snapshot()
        export_features(snapshot_path)
        metrics = run_training(snapshot_path)
        log_pipeline_run("success", snapshot_path, metrics)
        logger.info("Batch cycle completed successfully")
        return {
            "status": "success",
            "snapshot": str(snapshot_path),
            "climate_artifacts": str(len(climate_paths)),
            "economic_artifacts": str(len(economic_paths)),
            "regulatory_artifacts": str(len(regulatory_paths)),
            "metrics_summary": metrics,
        }
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Batch cycle failed: %s", exc, exc_info=True)
        log_pipeline_run("failure", Path("n/a"), {"series_modeled": 0, "alerts": 0})
        raise

