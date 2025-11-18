import argparse
import datetime as dt
import logging
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import pandas as pd

from ..external import configure_logging, ensure_directory

logger = configure_logging("antt_ingest")

LANDING_ROOT = Path("data/landing/external_factors-raw/logistics/antt")
DATE_CANDIDATES = (
    "date",
    "data",
    "competencia",
    "competência",
    "mes",
    "mês",
    "periodo",
    "período",
    "ano_mes",
    "reference",
)
STRING_DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%m/%Y", "%Y%m", "%Y")


def _read_source(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".csv", ".txt"}:
        return pd.read_csv(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file extension for {path}")


def _detect_date_column(df: pd.DataFrame) -> Tuple[str, pd.Series]:
    for candidate in DATE_CANDIDATES:
        if candidate in df.columns:
            series = df[candidate]
            return candidate, series
        for col in df.columns:
            if col.lower().strip().replace(" ", "_") == candidate:
                return col, df[col]

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            return col, df[col]

    for col in df.columns:
        if df[col].dtype == object:
            try:
                return col, pd.to_datetime(df[col], errors="raise")
            except Exception:
                continue

    raise ValueError("Could not detect a date column. Provide a CSV/XLSX with an explicit date/period column.")


def _normalize_dates(series: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(series):
        return pd.to_datetime(series).dt.date

    for fmt in STRING_DATE_FORMATS:
        try:
            parsed = pd.to_datetime(series, format=fmt, errors="raise")
            return parsed.dt.date
        except Exception:
            continue

    parsed = pd.to_datetime(series, errors="coerce")
    if parsed.isna().all():
        raise ValueError("Unable to parse dates from provided column.")
    return parsed.dt.date


def _melt_value_columns(df: pd.DataFrame, date_col: str, indicator: str) -> pd.DataFrame:
    numeric_cols = [col for col in df.columns if col != date_col and pd.api.types.is_numeric_dtype(df[col])]

    if not numeric_cols:
        non_numeric = [col for col in df.columns if col != date_col]
        raise ValueError(
            f"No numeric columns detected for indicator '{indicator}'. "
            f"Found columns: {non_numeric or df.columns.tolist()}"
        )

    if len(numeric_cols) == 1:
        values = df[[date_col, numeric_cols[0]]].rename(columns={numeric_cols[0]: "value"})
        values["metric"] = indicator
        return values

    melted = df[[date_col] + numeric_cols].melt(id_vars=date_col, var_name="metric", value_name="value")
    melted["metric"] = melted["metric"].fillna(indicator)
    return melted


def ingest_antt_file(source_path: Path, indicator: str, run_stamp: str) -> Path:
    logger.info("Ingesting ANTT indicator '%s' from %s", indicator, source_path)
    df = _read_source(source_path)
    if df.empty:
        raise ValueError("Source file is empty.")

    date_col, date_series = _detect_date_column(df)
    df = df.copy()
    df[date_col] = _normalize_dates(date_series)
    df = df.dropna(subset=[date_col])

    normalized = _melt_value_columns(df, date_col, indicator)
    normalized = normalized.dropna(subset=["value"])
    normalized = normalized.sort_values(date_col)
    normalized = normalized.rename(columns={date_col: "date"})
    normalized["indicator"] = indicator

    output_dir = LANDING_ROOT / indicator / run_stamp
    ensure_directory(output_dir)
    output_path = output_dir / f"{indicator}.csv"
    normalized[["date", "indicator", "metric", "value"]].to_csv(output_path, index=False)

    logger.info("Saved %s rows to %s", len(normalized), output_path)
    return output_path


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest manually downloaded ANTT logistics indicators.")
    parser.add_argument("--source", type=Path, required=True, help="Path to the raw ANTT CSV/XLSX file.")
    parser.add_argument("--indicator", type=str, default=None, help="Slug name for the indicator (default: filename stem).")
    parser.add_argument(
        "--timestamp",
        type=str,
        default=None,
        help="Override output timestamp (YYYYMMDD). Defaults to current UTC date.",
    )
    return parser.parse_args(args)


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    indicator = options.indicator or options.source.stem.lower().replace(" ", "_")
    run_stamp = options.timestamp or dt.datetime.utcnow().strftime("%Y%m%d")
    ingest_antt_file(options.source, indicator, run_stamp)


if __name__ == "__main__":
    main()

