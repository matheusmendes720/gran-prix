"""
Transform external raw datasets into Silver-layer parquet tables for ML usage.

This script reads the landing zone (`data/landing/external_factors-raw/`),
converts JSON payloads into normalized pandas DataFrames, filters data to the
desired historical window (default 2021 onward), and writes parquet files into
`data/silver/external_factors/`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

import pandas as pd

from . import configure_logging, ensure_directory
from .validation.logistics_dataset_checks import validate_all as validate_logistics_datasets
from scripts.automation.freight_blockers.integration import FreightBlockersETLStep


logger = configure_logging("silver_transform")

LANDING_ROOT = Path("data/landing/external_factors-raw")
SILVER_ROOT = Path("data/silver/external_factors")
START_DATE = pd.Timestamp("2021-01-01")


def write_parquet(df: pd.DataFrame, path: Path) -> None:
    if df.empty:
        logger.warning("Skipping parquet write for %s because dataframe is empty.", path)
        return
    ensure_directory(path.parent)
    df.to_parquet(path, index=False)
    logger.info("Wrote %s rows to %s", len(df), path)


# ---------------------------------------------------------------------------
# BACEN (PTAX + Selic)
# ---------------------------------------------------------------------------


def load_bacen_ptax() -> pd.DataFrame:
    base_dir = LANDING_ROOT / "macro" / "bacen" / "ptax"
    records: List[pd.DataFrame] = []

    if not base_dir.exists():
        logger.warning("PTAX directory %s does not exist.", base_dir)
        return pd.DataFrame()

    for currency_dir in base_dir.iterdir():
        if not currency_dir.is_dir():
            continue
        currency = currency_dir.name
        for run_dir in currency_dir.iterdir():
            json_path = run_dir / "ptax.json"
            if not json_path.exists():
                continue
            with json_path.open("r", encoding="utf-8") as fp:
                payload = json.load(fp)
            values = payload.get("value", [])
            if not values:
                continue
            df = pd.DataFrame(values)
            df["currency"] = currency.upper()
            df["run_date"] = pd.to_datetime(run_dir.name)
            df["dataHoraCotacao"] = pd.to_datetime(df["dataHoraCotacao"])
            records.append(df)

    if not records:
        return pd.DataFrame()

    df_all = pd.concat(records, ignore_index=True)
    df_all = df_all[df_all["dataHoraCotacao"] >= START_DATE]
    df_all.sort_values(["currency", "dataHoraCotacao"], inplace=True)
    return df_all


def load_bacen_selic() -> pd.DataFrame:
    json_path = LANDING_ROOT / "macro" / "bacen" / "selic"
    records = []

    if not json_path.exists():
        logger.warning("Selic directory %s does not exist.", json_path)
        return pd.DataFrame()

    for run_dir in json_path.iterdir():
        file_path = run_dir / "selic.json"
        if not file_path.exists():
            continue
        with file_path.open("r", encoding="utf-8") as fp:
            payload = json.load(fp)
        data = payload.get("data", [])
        if not data:
            continue
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
        df["selic"] = pd.to_numeric(df["valor"], errors="coerce")
        df["run_date"] = pd.to_datetime(run_dir.name)
        records.append(df[["date", "selic", "run_date"]])

    if not records:
        return pd.DataFrame()

    df_all = pd.concat(records, ignore_index=True)
    df_all = df_all[df_all["date"] >= START_DATE]
    df_all.sort_values("date", inplace=True)
    df_all.drop_duplicates(subset="date", keep="last", inplace=True)
    return df_all


# ---------------------------------------------------------------------------
# IBGE SIDRA helpers
# ---------------------------------------------------------------------------


def _load_ibge_series(slug: str, value_col: str, freq: str) -> pd.DataFrame:
    base_dir = LANDING_ROOT / "macro" / "ibge" / slug
    if not base_dir.exists():
        logger.warning("IBGE directory %s does not exist.", base_dir)
        return pd.DataFrame()

    frames = []
    for run_dir in sorted(base_dir.iterdir()):
        json_path = run_dir / f"{slug}.json"
        if not json_path.exists():
            continue
        with json_path.open("r", encoding="utf-8") as fp:
            payload = json.load(fp)
        if not isinstance(payload, list) or len(payload) <= 1:
            continue
        df = pd.DataFrame(payload[1:])

        period_col = "D3C"
        if "D4C" in df.columns and df["D4C"].astype(str).str.fullmatch(r"\d{6}").all():
            period_col = "D4C"

        codes = df[period_col].astype(str)
        if freq == "monthly":
            period = pd.to_datetime(codes, format="%Y%m")
        elif freq == "quarterly":
            year = codes.str.slice(0, 4).astype(int)
            quarter = codes.str.slice(4, 6).astype(int)
            period = pd.PeriodIndex.from_fields(year=year, quarter=quarter, freq="Q").to_timestamp(how="end")
        elif freq == "annual":
            period = pd.to_datetime(codes, format="%Y")
        else:
            raise ValueError(f"Unsupported frequency {freq}")

        series = pd.DataFrame(
            {
                "period": period,
                value_col: pd.to_numeric(df["V"], errors="coerce"),
                "run_date": pd.to_datetime(run_dir.name, errors="coerce"),
            }
        )
        frames.append(series)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.dropna(subset=["period"])
    combined.sort_values(["period", "run_date"], inplace=True)
    combined = combined.drop_duplicates(subset="period", keep="last")
    return combined


def load_ibge_ipca() -> pd.DataFrame:
    df = _load_ibge_series("ipca", "ipca", "monthly")
    if df.empty:
        return df
    df = df[df["period"] >= START_DATE]
    return df


def load_ibge_ipca15() -> pd.DataFrame:
    df = _load_ibge_series("ipca15", "ipca15", "monthly")
    if df.empty:
        return df
    df = df[df["period"] >= START_DATE]
    return df


def load_ibge_inpc() -> pd.DataFrame:
    df = _load_ibge_series("inpc", "inpc", "monthly")
    if df.empty:
        return df
    df = df[df["period"] >= START_DATE]
    return df


def load_ibge_unemployment() -> pd.DataFrame:
    df = _load_ibge_series("unemployment", "unemployment_rate", "monthly")
    if df.empty:
        return df
    df = df[df["period"] >= START_DATE]
    return df


def load_ibge_pib_quarterly() -> pd.DataFrame:
    df = _load_ibge_series("pib_quarterly", "pib_quarterly_yoy", "quarterly")
    if df.empty:
        return df
    return df


def load_ibge_pib_annual() -> pd.DataFrame:
    df = _load_ibge_series("pib_annual", "pib_annual_current_brl", "annual")
    if df.empty:
        return df
    return df


def load_fred_series(slug: str, value_col: str, freq: str) -> pd.DataFrame:
    base_dir = LANDING_ROOT / "macro" / "fred" / slug
    if not base_dir.exists():
        logger.warning("FRED directory %s missing.", base_dir)
        return pd.DataFrame()

    frames = []
    for run_dir in base_dir.iterdir():
        json_path = run_dir / f"{slug}.json"
        if not json_path.exists():
            continue
        with json_path.open("r", encoding="utf-8") as fp:
            payload = json.load(fp)
        df = pd.DataFrame(payload)
        if df.empty:
            continue
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["run_date"] = pd.to_datetime(run_dir.name, errors="coerce")
        frames.append(df[["date", "value", "run_date"]])

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.dropna(subset=["date"])
    combined.sort_values(["date", "run_date"], inplace=True)
    combined = combined.drop_duplicates(subset="date", keep="last")

    if freq == "monthly":
        combined["date"] = combined["date"] + pd.offsets.MonthEnd(0)
    elif freq == "annual":
        combined["date"] = combined["date"] + pd.offsets.YearEnd(0)

    combined = combined.rename(columns={"value": value_col})
    return combined


# ---------------------------------------------------------------------------
# World Bank
# ---------------------------------------------------------------------------


def load_worldbank_indicator(slug: str) -> pd.DataFrame:
    base_dir = LANDING_ROOT / "global" / "worldbank" / slug
    if not base_dir.exists():
        logger.warning("World Bank directory %s missing.", base_dir)
        return pd.DataFrame()

    dfs = []
    for run_dir in base_dir.iterdir():
        json_path = run_dir / f"{slug}.json"
        if not json_path.exists():
            continue
        with json_path.open("r", encoding="utf-8") as fp:
            payload = json.load(fp)
        if len(payload) < 2:
            continue
        data = payload[1]
        df = pd.DataFrame(data)
        df["date"] = pd.to_numeric(df["date"], errors="coerce")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["run_date"] = pd.to_datetime(run_dir.name)
        df = df.dropna(subset=["date"])
        df["year"] = df["date"].astype(int)
        dfs.append(df[["year", "value", "run_date"]])

    if not dfs:
        return pd.DataFrame()

    df_all = pd.concat(dfs, ignore_index=True)
    df_all.sort_values(["year", "run_date"], inplace=True)
    df_latest = df_all.drop_duplicates(subset="year", keep="last")
    df_latest["value"] = pd.to_numeric(df_latest["value"], errors="coerce")
    df_latest = df_latest[df_latest["year"] >= START_DATE.year - 5]
    df_latest.sort_values("year", inplace=True)
    df_latest["value"] = df_latest["value"].ffill()
    df_latest = df_latest[df_latest["year"] >= START_DATE.year]
    return df_latest


# ---------------------------------------------------------------------------
# OpenWeather / Open-Meteo
# ---------------------------------------------------------------------------


def load_openmeteo_history() -> pd.DataFrame:
    base_dir = LANDING_ROOT / "openweather"
    if not base_dir.exists():
        logger.warning("OpenWeather directory %s missing.", base_dir)
        return pd.DataFrame()

    records = []
    for city_dir in base_dir.iterdir():
        if not city_dir.is_dir():
            continue
        city_slug = city_dir.name
        for run_dir in city_dir.iterdir():
            history_path = run_dir / "openmeteo_history.json"
            if not history_path.exists():
                continue
            with history_path.open("r", encoding="utf-8") as fp:
                payload = json.load(fp)
            hourly = payload.get("hourly", {})
            times = hourly.get("time", [])
            if not times:
                continue
            df = pd.DataFrame(hourly)
            df["timestamp"] = pd.to_datetime(df["time"])
            df["city"] = city_slug
            df["run_date"] = pd.to_datetime(run_dir.name)
            df = df[df["timestamp"] >= START_DATE]
            records.append(df)

    if not records:
        return pd.DataFrame()

    df_all = pd.concat(records, ignore_index=True)
    df_all.sort_values(["city", "timestamp"], inplace=True)
    df_all["date"] = df_all["timestamp"].dt.date
    df_daily = (
        df_all.groupby(["city", "date"])
        .agg(
            temperature_2m_daily=("temperature_2m", "mean"),
            relative_humidity_2m_daily=("relative_humidity_2m", "mean"),
            precipitation_daily=("precipitation", "sum"),
            wind_speed_10m_daily=("wind_speed_10m", "mean"),
        )
        .reset_index()
    )
    df_daily["date"] = pd.to_datetime(df_daily["date"])
    return df_daily


# ---------------------------------------------------------------------------
# ANP fuel prices
# ---------------------------------------------------------------------------


def load_anp_fuel() -> pd.DataFrame:
    base_dir = LANDING_ROOT / "logistics" / "anp_fuel"
    if not base_dir.exists():
        logger.warning("ANP directory %s missing.", base_dir)
        return pd.DataFrame()

    frames = []
    for run_dir in base_dir.iterdir():
        csv_path = run_dir / "anp_fuel.csv"
        if not csv_path.exists():
            continue
        df = pd.read_csv(csv_path, parse_dates=["date"])
        df["run_date"] = pd.to_datetime(run_dir.name)
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined[combined["date"] >= START_DATE]
    combined.sort_values(["date", "run_date"], inplace=True)
    combined = combined.drop_duplicates(subset="date", keep="last")
    combined.drop(columns=["run_date"], inplace=True)
    return combined


# ---------------------------------------------------------------------------
# Freight benchmarks (World Bank proxies)
# ---------------------------------------------------------------------------


def load_freight_benchmarks() -> pd.DataFrame:
    base_dir = LANDING_ROOT / "logistics" / "freight"
    if not base_dir.exists():
        logger.warning("Freight directory %s missing.", base_dir)
        return pd.DataFrame()

    frames = []
    for run_dir in base_dir.iterdir():
        for csv_path in run_dir.glob("*.csv"):
            df = pd.read_csv(csv_path, parse_dates=["date"])
            df["metric"] = df["metric"].astype(str)
            df["country"] = df["country"].astype(str)
            df["run_date"] = pd.to_datetime(run_dir.name)
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined[combined["date"] >= START_DATE]
    combined.sort_values(["metric", "country", "date", "run_date"], inplace=True)
    combined = combined.drop_duplicates(subset=["metric", "country", "date"], keep="last")

    pivoted = combined.pivot_table(index="date", columns=["metric", "country"], values="value")
    pivoted = pivoted.sort_index().reset_index()

    flat_columns = []
    for col in pivoted.columns:
        if col == "date":
            flat_columns.append("date")
        elif isinstance(col, tuple):
            metric, country = col
            flat_columns.append(f"{metric}_{country.lower()}")
        else:
            flat_columns.append(str(col))
    pivoted.columns = flat_columns
    if len(pivoted.columns) > 0 and pivoted.columns[0] != "date":
        pivoted.rename(columns={pivoted.columns[0]: "date"}, inplace=True)
    return pivoted


# ---------------------------------------------------------------------------
# Manual Freightos FBX
# ---------------------------------------------------------------------------


def load_freightos_fbx() -> pd.DataFrame:
    base_dir = LANDING_ROOT / "logistics" / "freightos"
    if not base_dir.exists():
        logger.warning("Freightos directory %s missing.", base_dir)
        return pd.DataFrame()

    frames = []
    for run_dir in base_dir.iterdir():
        csv_path = run_dir / "freightos_fbx.csv"
        if not csv_path.exists():
            continue
        df = pd.read_csv(csv_path, parse_dates=["date"])
        df["run_date"] = pd.to_datetime(run_dir.name)
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined[combined["date"] >= START_DATE]
    combined.sort_values(["date", "run_date"], inplace=True)
    combined = combined.drop_duplicates(subset="date", keep="last")
    combined.drop(columns=["run_date"], inplace=True)
    combined.rename(columns={"value": "freightos_fbx"}, inplace=True)
    return combined


# ---------------------------------------------------------------------------
# Manual Drewry WCI
# ---------------------------------------------------------------------------


def load_drewry_wci() -> pd.DataFrame:
    base_dir = LANDING_ROOT / "logistics" / "drewry"
    if not base_dir.exists():
        logger.warning("Drewry directory %s missing.", base_dir)
        return pd.DataFrame()

    frames = []
    for run_dir in base_dir.iterdir():
        csv_path = run_dir / "drewry_wci.csv"
        if not csv_path.exists():
            continue
        df = pd.read_csv(csv_path, parse_dates=["date"])
        df["run_date"] = pd.to_datetime(run_dir.name)
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined[combined["date"] >= START_DATE]
    combined.sort_values(["date", "run_date"], inplace=True)
    combined = combined.drop_duplicates(subset="date", keep="last")
    combined.drop(columns=["run_date"], inplace=True)
    combined.rename(columns={"value": "drewry_wci"}, inplace=True)
    return combined


# ---------------------------------------------------------------------------
# Baltic Dry Index (manual ingest)
# ---------------------------------------------------------------------------


def load_baltic_dry() -> pd.DataFrame:
    base_dir = LANDING_ROOT / "logistics" / "baltic_dry"
    if not base_dir.exists():
        logger.warning("Baltic Dry directory %s missing.", base_dir)
        return pd.DataFrame()

    frames = []
    for run_dir in base_dir.iterdir():
        csv_path = run_dir / "baltic_dry.csv"
        if not csv_path.exists():
            continue
        df = pd.read_csv(csv_path, parse_dates=["date"])
        df["run_date"] = pd.to_datetime(run_dir.name)
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined[combined["date"] >= START_DATE]
    combined.sort_values(["date", "run_date"], inplace=True)
    combined = combined.drop_duplicates(subset="date", keep="last")
    combined.drop(columns=["run_date"], inplace=True)
    combined.rename(columns={"value": "baltic_dry_index"}, inplace=True)
    return combined


# ---------------------------------------------------------------------------
# ANTT logistics indicators (manual ingest)
# ---------------------------------------------------------------------------


def load_antt_metrics() -> pd.DataFrame:
    base_dir = LANDING_ROOT / "logistics" / "antt"
    if not base_dir.exists():
        logger.warning("ANTT directory %s missing.", base_dir)
        return pd.DataFrame()

    frames = []
    for indicator_dir in base_dir.iterdir():
        if not indicator_dir.is_dir():
            continue
        indicator_slug = indicator_dir.name
        for run_dir in indicator_dir.iterdir():
            if not run_dir.is_dir():
                continue
            for csv_path in run_dir.glob("*.csv"):
                df = pd.read_csv(csv_path, parse_dates=["date"])
                df["indicator_slug"] = indicator_slug
                df["run_date"] = pd.to_datetime(run_dir.name, errors="coerce")
                frames.append(df)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined[combined["date"] >= START_DATE]
    combined.sort_values(["indicator_slug", "metric", "date", "run_date"], inplace=True)
    combined = combined.drop_duplicates(subset=["indicator_slug", "metric", "date"], keep="last")
    combined.drop(columns=["run_date"], inplace=True)

    combined["column"] = (
        combined["indicator_slug"]
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
        + "_"
        + combined["metric"]
        .astype(str)
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    pivoted = combined.pivot_table(index="date", columns="column", values="value")
    pivoted = pivoted.sort_index().reset_index()
    return pivoted


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------


def transform_all() -> None:
    logger.info("Starting Silver transformation for external factors.")

    ptax_df = load_bacen_ptax()
    write_parquet(ptax_df, SILVER_ROOT / "macro" / "ptax_rates.parquet")

    selic_df = load_bacen_selic()
    write_parquet(selic_df, SILVER_ROOT / "macro" / "selic_daily.parquet")

    ipca_df = load_ibge_ipca()
    write_parquet(ipca_df, SILVER_ROOT / "macro" / "ipca_monthly.parquet")

    ipca15_df = load_ibge_ipca15()
    write_parquet(ipca15_df, SILVER_ROOT / "macro" / "ipca15_monthly.parquet")

    inpc_df = load_ibge_inpc()
    write_parquet(inpc_df, SILVER_ROOT / "macro" / "inpc_monthly.parquet")

    unemployment_df = load_ibge_unemployment()
    write_parquet(unemployment_df, SILVER_ROOT / "macro" / "unemployment_rate.parquet")

    pib_q_df = load_ibge_pib_quarterly()
    write_parquet(pib_q_df, SILVER_ROOT / "macro" / "pib_quarterly_yoy.parquet")

    pib_a_df = load_ibge_pib_annual()
    write_parquet(pib_a_df, SILVER_ROOT / "macro" / "pib_annual_value.parquet")

    fred_cds_df = load_fred_series("cds", "cds_spread_bps", "monthly")
    write_parquet(fred_cds_df, SILVER_ROOT / "macro" / "cds_spread.parquet")

    fred_ppp_df = load_fred_series("ppp", "ppp_conversion_factor", "annual")
    write_parquet(fred_ppp_df, SILVER_ROOT / "macro" / "ppp_conversion_factor.parquet")

    for slug in ("gdp_current_usd", "gdp_ppp", "gdp_growth_pct"):
        wb_df = load_worldbank_indicator(slug)
        write_parquet(wb_df, SILVER_ROOT / "global" / f"{slug}.parquet")

    weather_df = load_openmeteo_history()
    write_parquet(weather_df, SILVER_ROOT / "climatic" / "openmeteo_daily.parquet")

    anp_df = load_anp_fuel()
    write_parquet(anp_df, SILVER_ROOT / "logistics" / "anp_fuel_daily.parquet")

    freight_df = load_freight_benchmarks()
    write_parquet(freight_df, SILVER_ROOT / "logistics" / "freight_worldbank.parquet")

    baltic_df = load_baltic_dry()
    write_parquet(baltic_df, SILVER_ROOT / "logistics" / "baltic_dry.parquet")

    fbx_df = load_freightos_fbx()
    write_parquet(fbx_df, SILVER_ROOT / "logistics" / "freightos_fbx.parquet")

    drewry_df = load_drewry_wci()
    write_parquet(drewry_df, SILVER_ROOT / "logistics" / "drewry_wci.parquet")

    antt_df = load_antt_metrics()
    write_parquet(antt_df, SILVER_ROOT / "logistics" / "antt_metrics.parquet")

    logger.info("Triggering freight blockers automation for Xeneta, SCFI/CCFI, and ANTT CKAN datasets.")
    try:
        FreightBlockersETLStep(output_dir="data/silver/freight").execute()
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Freight blockers automation failed: %s", exc)

    logger.info("Running logistics dataset validation checks...")
    if not validate_logistics_datasets():
        logger.warning("Logistics validation reported issues. Review logs above.")

    logger.info("Silver transformation finished.")


if __name__ == "__main__":
    transform_all()

