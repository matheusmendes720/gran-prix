from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import httpx
import polars as pl
from prefect import flow, get_run_logger, task

from demand_forecasting.validation.utils import write_validation_result
from demand_forecasting.validation.validators import validate_regulatory as ge_validate_regulatory

from .schemas import RegulatoryBulletin
from .utils import (
    PersistedArtifact,
    bronze_folder,
    load_env,
    silver_folder,
    write_json,
    write_manifest,
)


ANATEL_BULLETIN_URL = "https://api.anatel.gov.br/bulletins/latest"


def _stub_bulletin(period: date) -> dict:
    return {
        "issued_at": datetime.utcnow().isoformat(),
        "source": "stub",
        "items": [
            {
                "regulation_id": f"R-{period:%Y%m}",
                "title": "Placeholder regulation",
                "effective_date": period.replace(day=1).isoformat(),
                "summary": "No regulatory changes - stub data",
                "jurisdiction": "ANATEL",
            }
        ],
    }


@task(retries=3, retry_delay_seconds=120)
def fetch_regulatory_bulletin(period: date) -> dict:
    token = load_env("ANATEL_API_TOKEN", required=False)
    if not token:
        return _stub_bulletin(period)

    headers = {"Authorization": f"Bearer {token}"}
    params = {"period": period.strftime("%Y-%m")}
    with httpx.Client(timeout=60.0) as client:
        response = client.get(ANATEL_BULLETIN_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


@task
def validate_bulletin(raw_payload: dict) -> RegulatoryBulletin:
    return RegulatoryBulletin.model_validate(raw_payload)


@task
def persist_regulatory_raw(period: date, bulletin: RegulatoryBulletin) -> PersistedArtifact:
    folder = bronze_folder("regulatory", period.replace(day=1))
    path = folder / "bulletin.json"
    write_json(bulletin.model_dump(mode="json"), path)
    return PersistedArtifact(
        domain="regulatory",
        layer="bronze",
        path=path,
        record_count=len(bulletin.items),
        metadata={"period": period.strftime("%Y-%m")},
    )


@task
def persist_regulatory_silver(period: date, bulletin: RegulatoryBulletin) -> PersistedArtifact:
    folder = silver_folder("regulatory", period.replace(day=1))
    file_name = f"regulatory-{period.strftime('%Y-%m')}.parquet"
    path = folder / file_name
    df = pl.from_dicts(
        [item.model_dump() for item in bulletin.items],
        schema={
            "regulation_id": pl.String,
            "title": pl.String,
            "effective_date": pl.Date,
            "summary": pl.String,
            "jurisdiction": pl.String,
        },
    )
    df.write_parquet(path)
    return PersistedArtifact(
        domain="regulatory",
        layer="silver",
        path=path,
        record_count=df.height,
        metadata={"period": period.strftime("%Y-%m")},
    )


@task
def validate_regulatory_silver(period: date, bulletin: RegulatoryBulletin) -> str:
    df = pl.from_dicts(
        [item.model_dump() for item in bulletin.items],
        schema={
            "regulation_id": pl.String,
            "title": pl.String,
            "effective_date": pl.Date,
            "summary": pl.String,
            "jurisdiction": pl.String,
        },
    )
    payload = ge_validate_regulatory(df.to_pandas())
    payload["metadata"] = {"period": period.strftime("%Y-%m")}
    log_path = write_validation_result(f"regulatory-{period.strftime('%Y-%m')}", payload)
    return log_path.as_posix()


@task
def write_regulatory_manifest(period: date, artifacts: list[PersistedArtifact]) -> Path:
    entries = [artifact.to_manifest_entry() for artifact in artifacts]
    return write_manifest("regulatory", period.replace(day=1), entries)


@flow(name="ingest-regulatory")
def regulatory_ingestion_flow(period: date | None = None) -> list[str]:
    logger = get_run_logger()
    period = period or date.today()

    raw_payload = fetch_regulatory_bulletin(period)
    bulletin = validate_bulletin(raw_payload)
    bronze_artifact = persist_regulatory_raw(period, bulletin)
    silver_artifact = persist_regulatory_silver(period, bulletin)
    validation_log = validate_regulatory_silver(period, bulletin)
    manifest = write_regulatory_manifest(period, [bronze_artifact, silver_artifact])
    logger.info("Regulatory manifest stored at %s", manifest)
    logger.info("Regulatory validation log stored at %s", validation_log)
    return [bronze_artifact.path.as_posix(), silver_artifact.path.as_posix()]


__all__ = ["regulatory_ingestion_flow"]

