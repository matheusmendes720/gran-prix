from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Iterable

import httpx
import polars as pl
from prefect import flow, get_run_logger, task

from demand_forecasting.validation.utils import write_validation_result
from demand_forecasting.validation.validators import validate_climate as ge_validate_climate

from .schemas import ClimateDailyReading, ClimateForecast
from .utils import (
    PersistedArtifact,
    bronze_folder,
    load_env,
    silver_folder,
    write_json,
    write_manifest,
)


DEFAULT_REGIONS = ["bahia", "ceara", "pernambuco"]
INMET_BASE_URL = "https://apitempo.inmet.gov.br/v1/previsao"


def _stub_climate_payload(region: str, run_date: date) -> dict:
    days = []
    for offset in range(0, 3):
        current = run_date.toordinal() + offset
        days.append(
            {
                "date": date.fromordinal(current).isoformat(),
                "temp_min": 20.0 + offset,
                "temp_max": 30.0 + offset,
                "precipitation": float(offset),
                "wind_speed": 12.0,
                "humidity": 70.0,
            }
        )
    return {
        "region": region,
        "updated_at": datetime.utcnow().isoformat(),
        "days": days,
    }


@task(retries=3, retry_delay_seconds=60)
def fetch_climate(region: str, run_date: date) -> dict:
    logger = get_run_logger()
    token = load_env("INMET_API_TOKEN", required=False)
    if not token:
        logger.warning(
            "INMET_API_TOKEN not set, generating stub climate payload for region '%s'", region
        )
        return _stub_climate_payload(region, run_date)

    params = {"data": run_date.isoformat(), "token": token}
    url = f"{INMET_BASE_URL}/{region}"
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        # Real API returns nested structures per municipality; adapt accordingly
        payload = response.json()

    logger.info("Fetched climate payload for region %s", region)
    return payload


@task
def validate_climate(raw_payload: dict) -> ClimateForecast:
    return ClimateForecast.model_validate(raw_payload)


@task
def persist_climate_raw(region: str, run_date: date, payload: ClimateForecast) -> PersistedArtifact:
    folder = bronze_folder("climate", run_date, qualifier=region)
    path = folder / "forecast.json"
    write_json(payload.model_dump(mode="json"), path)
    return PersistedArtifact(
        domain="climate",
        layer="bronze",
        path=path,
        record_count=len(payload.days),
        metadata={"region": region},
    )


def _climate_rows(region: str, forecast: ClimateForecast) -> Iterable[dict]:
    for day in forecast.days:
        day: ClimateDailyReading
        yield {
            "region": region,
            "date": day.date,
            "temp_min_c": day.temp_min_c,
            "temp_max_c": day.temp_max_c,
            "precipitation_mm": day.precipitation_mm,
            "wind_speed_kmh": day.wind_speed_kmh,
            "humidity_pct": day.humidity_pct,
            "updated_at": forecast.updated_at,
        }


def _climate_frame(region: str, forecast: ClimateForecast) -> pl.DataFrame:
    return pl.from_dicts(
        list(_climate_rows(region, forecast)),
        schema={
            "region": pl.String,
            "date": pl.Date,
            "temp_min_c": pl.Float64,
            "temp_max_c": pl.Float64,
            "precipitation_mm": pl.Float64,
            "wind_speed_kmh": pl.Float64,
            "humidity_pct": pl.Float64,
            "updated_at": pl.Datetime,
        },
    )


@task
def persist_climate_silver(run_date: date, region: str, forecast: ClimateForecast) -> PersistedArtifact:
    folder = silver_folder("climate", run_date)
    path = folder / f"climate-{region}.parquet"
    df = _climate_frame(region, forecast)
    df.write_parquet(path)
    return PersistedArtifact(
        domain="climate",
        layer="silver",
        path=path,
        record_count=df.height,
        metadata={"region": region},
    )


@task
def validate_climate_silver(run_date: date, region: str, forecast: ClimateForecast) -> str:
    df = _climate_frame(region, forecast)
    payload = ge_validate_climate(df.to_pandas(), run_date)
    payload["metadata"] = {"region": region, "run_date": run_date.isoformat()}
    log_path = write_validation_result(f"climate-{region}", payload)
    return log_path.as_posix()


@task
def record_manifest(run_date: date, artifacts: list[PersistedArtifact]) -> Path:
    entries = [artifact.to_manifest_entry() for artifact in artifacts]
    return write_manifest("climate", run_date, entries)


@flow(name="ingest-climate")
def climate_ingestion_flow(run_date: date | None = None, regions: list[str] | None = None) -> list[str]:
    run_date = run_date or date.today()
    regions = regions or DEFAULT_REGIONS
    logger = get_run_logger()

    artifacts: list[PersistedArtifact] = []
    validation_logs: list[str] = []
    for region in regions:
        raw_payload = fetch_climate(region, run_date)
        forecast = validate_climate(raw_payload)
        raw_artifact = persist_climate_raw(region, run_date, forecast)
        silver_artifact = persist_climate_silver(run_date, region, forecast)
        validation_log = validate_climate_silver(run_date, region, forecast)
        artifacts.extend([raw_artifact, silver_artifact])
        validation_logs.append(validation_log)

    manifest = record_manifest(run_date, artifacts)
    logger.info("Wrote climate manifest to %s", manifest)
    logger.info("Climate validation logs stored: %s", validation_logs)
    return [artifact.path.as_posix() for artifact in artifacts]


__all__ = ["climate_ingestion_flow"]

