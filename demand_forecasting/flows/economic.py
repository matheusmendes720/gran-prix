from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import httpx
import polars as pl
from prefect import flow, get_run_logger, task

from demand_forecasting.validation.utils import write_validation_result
from demand_forecasting.validation.validators import validate_economic as ge_validate_economic

from .schemas import EconomicIndicator, EconomicSnapshot
from .utils import (
    PersistedArtifact,
    bronze_folder,
    load_env,
    silver_folder,
    write_json,
    write_manifest,
)


BACEN_BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series}/dados/ultimos/{count}"
IBGE_IPCA_URL = "https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/63/p/all/d/v63%200"

DEFAULT_SERIES = {
    "ptax": 1,
    "selic": 4390,
}


def _stub_economic_payload(week_end: date) -> dict:
    series = []
    for name in ("ptax", "selic"):
        series.append(
            {
                "name": name,
                "value": 5.0 if name == "selic" else 4.95,
                "unit": "percent" if name == "selic" else "brl/usd",
                "observed_at": week_end.isoformat(),
            }
        )
    return {
        "series": series,
        "source": "stub",
        "week_end": week_end.isoformat(),
    }


@task(retries=3, retry_delay_seconds=60)
def fetch_bacen_series(series_id: int, count: int = 7) -> list[dict]:
    token = load_env("BACEN_API_TOKEN", required=False)
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = BACEN_BASE_URL.format(series=series_id, count=count)
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


@task
def merge_economic_payload(week_end: date) -> dict:
    token = load_env("BACEN_API_TOKEN", required=False)
    if not token:
        return _stub_economic_payload(week_end)

    records: list[dict] = []
    for name, series_id in DEFAULT_SERIES.items():
        payload = fetch_bacen_series(series_id)
        for row in payload:
            records.append(
                {
                    "name": name,
                    "value": float(row["valor"]),
                    "unit": "percent" if name == "selic" else "brl/usd",
                    "observed_at": datetime.strptime(row["data"], "%d/%m/%Y").date().isoformat(),
                }
            )

    return {
        "series": records,
        "source": "bacen",
        "week_end": week_end.isoformat(),
    }


@task
def validate_snapshot(raw_payload: dict) -> EconomicSnapshot:
    return EconomicSnapshot.model_validate(raw_payload)


@task
def persist_economic_raw(week_end: date, snapshot: EconomicSnapshot) -> PersistedArtifact:
    folder = bronze_folder("economic", week_end)
    path = folder / "snapshot.json"
    write_json(snapshot.model_dump(mode="json"), path)
    return PersistedArtifact(
        domain="economic",
        layer="bronze",
        path=path,
        record_count=len(snapshot.series),
        metadata={"week_end": week_end.isoformat()},
    )


@task
def persist_economic_silver(week_end: date, snapshot: EconomicSnapshot) -> PersistedArtifact:
    folder = silver_folder("economic", week_end)
    path = folder / f"economic-{week_end.isoformat()}.parquet"
    df = pl.from_dicts(
        [indicator.model_dump() for indicator in snapshot.series],
        schema={
            "name": pl.String,
            "value": pl.Float64,
            "observed_at": pl.Date,
            "unit": pl.String,
        },
    ).with_columns(pl.lit(snapshot.source).alias("source"))
    df.write_parquet(path)
    return PersistedArtifact(
        domain="economic",
        layer="silver",
        path=path,
        record_count=df.height,
        metadata={"week_end": week_end.isoformat()},
    )


@task
def validate_economic_silver(week_end: date, snapshot: EconomicSnapshot) -> str:
    df = pl.from_dicts(
        [indicator.model_dump() for indicator in snapshot.series],
        schema={
            "name": pl.String,
            "value": pl.Float64,
            "observed_at": pl.Date,
            "unit": pl.String,
        },
    ).with_columns(pl.lit(snapshot.source).alias("source"))

    payload = ge_validate_economic(df.to_pandas())
    payload["metadata"] = {"week_end": week_end.isoformat()}
    log_path = write_validation_result(f"economic-{week_end.isoformat()}", payload)
    return log_path.as_posix()


@task
def write_economic_manifest(week_end: date, artifacts: list[PersistedArtifact]) -> Path:
    entries = [artifact.to_manifest_entry() for artifact in artifacts]
    return write_manifest("economic", week_end, entries)


@flow(name="ingest-economic")
def economic_ingestion_flow(week_end: date | None = None) -> list[str]:
    logger = get_run_logger()
    week_end = week_end or (date.today() - timedelta(days=date.today().weekday()))

    raw_payload = merge_economic_payload(week_end)
    snapshot = validate_snapshot(raw_payload)
    bronze_artifact = persist_economic_raw(week_end, snapshot)
    silver_artifact = persist_economic_silver(week_end, snapshot)
    validation_log = validate_economic_silver(week_end, snapshot)
    manifest_path = write_economic_manifest(week_end, [bronze_artifact, silver_artifact])
    logger.info("Economic manifest stored at %s", manifest_path)
    logger.info("Economic validation log stored at %s", validation_log)
    return [bronze_artifact.path.as_posix(), silver_artifact.path.as_posix()]


__all__ = ["economic_ingestion_flow"]

