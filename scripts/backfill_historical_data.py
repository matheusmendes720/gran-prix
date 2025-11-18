"""Historical backfill builder for Nova Corrente demand forecasting pipeline.

Generates a surrogate timeline (2019-01-01 → <actual_start) using the internal
enrichment datasets only, producing `data/processed/nova_corrente/
nova_corrente_fact_backfill.parquet`.

Usage:
    python scripts/backfill_historical_data.py
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

import polars as pl

# Ensure project root is on PYTHONPATH when running as a script
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from demand_forecasting.validation.validators import validate_fact_backfill


DATA_ROOT = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_ROOT / "processed"
BACKFILL_OUTPUT = PROCESSED_DIR / "nova_corrente" / "nova_corrente_fact_backfill.parquet"
SUMMARY_DIR = DATA_ROOT / "outputs" / "nova_corrente" / "historical_backfill"
VALIDATION_LOG_DIR = PROJECT_ROOT / "logs" / "pipeline" / "validation"


def _write_validation_result(name: str, payload: dict) -> Path:
    VALIDATION_LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = VALIDATION_LOG_DIR / f"{timestamp}-{name}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def _load_actual() -> pl.DataFrame:
    path = PROCESSED_DIR / "nova_corrente" / "nova_corrente_processed.csv"
    df = pl.read_csv(path, try_parse_dates=True)
    return _ensure_date(df)


def _load_enrichment() -> pl.DataFrame:
    path = PROCESSED_DIR / "unified_brazilian_telecom_nova_corrente_enriched.csv"
    df = pl.read_csv(path, try_parse_dates=True)
    return _ensure_date(df)


def _ensure_date(df: pl.DataFrame) -> pl.DataFrame:
    if df.schema.get("date") == pl.Date:
        return df
    return df.with_columns(pl.col("date").str.strptime(pl.Date, strict=False))


def _family_stats(actual: pl.DataFrame) -> tuple[pl.DataFrame, float, float]:
    family = (
        actual.group_by("familia")
        .agg(
            pl.col("quantidade").mean().alias("family_avg_qty"),
            pl.col("lead_time_days").mean().alias("family_avg_lead"),
        )
        .with_columns(
            pl.when(pl.col("family_avg_qty") <= 0)
            .then(pl.lit(1.0))
            .otherwise(pl.col("family_avg_qty"))
            .alias("family_avg_qty"),
        )
    )

    overall_qty = float(actual["quantidade"].mean())
    overall_lead = float(actual["lead_time_days"].mean())
    return family, overall_qty, overall_lead


def _combo_stats(actual: pl.DataFrame) -> pl.DataFrame:
    return (
        actual.group_by(["item_id", "site_id"])
        .agg(
            pl.col("material").first(),
            pl.col("familia").first(),
            pl.col("category").first(),
            pl.col("unidade_medida").first(),
            pl.col("deposito").first(),
            pl.col("fornecedor").first(),
            pl.col("quantidade").mean().alias("avg_qty"),
            pl.col("quantidade").median().alias("median_qty"),
            pl.col("lead_time_days").mean().alias("avg_lead_time"),
        )
        .with_columns(
            pl.col("avg_qty").fill_null(pl.col("median_qty")),
            pl.col("avg_lead_time").fill_null(pl.lit(None, pl.Float64)),
        )
    )


def _seasonality_factors(actual: pl.DataFrame, family_stats: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
    weekday = (
        actual.with_columns(pl.col("date").dt.weekday().alias("weekday"))
        .group_by(["familia", "weekday"])
        .agg(pl.col("quantidade").mean().alias("weekday_mean"))
    )
    month = (
        actual.with_columns(pl.col("date").dt.month().alias("month"))
        .group_by(["familia", "month"])
        .agg(pl.col("quantidade").mean().alias("month_mean"))
    )

    weekday_factor = (
        weekday.join(family_stats.select(["familia", "family_avg_qty"]), on="familia", how="left")
        .with_columns(
            (
                pl.when(pl.col("family_avg_qty") <= 0)
                .then(pl.lit(1.0))
                .otherwise(pl.col("weekday_mean") / pl.col("family_avg_qty"))
            )
            .alias("weekday_factor")
        )
        .select(["familia", "weekday", "weekday_factor"])
    )

    month_factor = (
        month.join(family_stats.select(["familia", "family_avg_qty"]), on="familia", how="left")
        .with_columns(
            (
                pl.when(pl.col("family_avg_qty") <= 0)
                .then(pl.lit(1.0))
                .otherwise(pl.col("month_mean") / pl.col("family_avg_qty"))
            )
            .alias("month_factor")
        )
        .select(["familia", "month", "month_factor"])
    )

    return (
        weekday_factor.with_columns(pl.col("weekday_factor").fill_nan(1.0).fill_null(1.0)),
        month_factor.with_columns(pl.col("month_factor").fill_nan(1.0).fill_null(1.0)),
    )


def _prepare_context(enriched: pl.DataFrame, actual_start: date) -> pl.DataFrame:
    context = (
        enriched.filter(pl.col("date") < pl.lit(actual_start))
        .group_by("date", maintain_order=True)
        .agg(pl.all().first())
        .with_columns(
            pl.col("demand_multiplier").fill_null(1.0),
            pl.col("regional_demand_multiplier").fill_null(1.0),
            pl.col("new_component_demand_multiplier").fill_null(1.0),
            pl.col("old_component_demand_multiplier").fill_null(1.0),
            pl.col("base_lead_time_days").fill_null(pl.col("total_lead_time_days")),
            pl.col("total_lead_time_days").fill_null(pl.col("base_lead_time_days")),
            pl.col("date").dt.weekday().alias("weekday"),
            pl.col("date").dt.month().alias("month"),
        )
    )
    return context


def _deterministic_jitter() -> pl.Expr:
    key = (
        pl.col("item_id").cast(pl.Utf8)
        + pl.lit("|")
        + pl.col("site_id").cast(pl.Utf8)
        + pl.lit("|")
        + pl.col("date").cast(pl.Utf8)
    )
    return (
        key.hash()
        .cast(pl.Float64)
        .truediv(2**64)
        .sub(0.5)
        .mul(0.02)
        .add(1.0)
    )


def build_backfill() -> tuple[pl.DataFrame, date]:
    actual = _load_actual()
    enriched = _load_enrichment()

    if actual.is_empty():
        raise RuntimeError("Actual Nova Corrente dataset is empty; cannot build backfill.")

    actual_start = actual["date"].min()
    family_stats, overall_qty, overall_lead = _family_stats(actual)
    combos = _combo_stats(actual).join(family_stats, on="familia", how="left")
    weekday_factor, month_factor = _seasonality_factors(actual, family_stats)
    context = _prepare_context(enriched, actual_start)

    if context.is_empty():
        raise RuntimeError("Context frame empty — check enrichment dataset coverage.")

    base_qty = (
        pl.coalesce(
            [
                pl.col("avg_qty"),
                pl.col("median_qty"),
                pl.col("family_avg_qty"),
                pl.lit(overall_qty),
            ]
        )
        .clip(0.0, None)
    )
    lead_base = pl.coalesce(
        [
            pl.col("avg_lead_time"),
            pl.col("family_avg_lead"),
            pl.lit(overall_lead),
        ]
    )

    backfill = (
        combos.lazy()
        .join(context.lazy(), how="cross")
        .join(weekday_factor.lazy(), on=["familia", "weekday"], how="left")
        .join(month_factor.lazy(), on=["familia", "month"], how="left")
        .with_columns(
            base_qty.alias("baseline_qty"),
            lead_base.alias("baseline_lead"),
            pl.col("weekday_factor").fill_null(1.0),
            pl.col("month_factor").fill_null(1.0),
        )
        .with_columns(
            (pl.col("weekday_factor") * pl.col("month_factor")).alias("seasonality_factor"),
            (
                pl.col("demand_multiplier")
                * pl.col("regional_demand_multiplier")
                * pl.col("new_component_demand_multiplier")
                * pl.col("old_component_demand_multiplier")
            ).alias("context_factor"),
        )
        .with_columns(
            (_deterministic_jitter() * pl.col("seasonality_factor") * pl.col("context_factor") * pl.col("baseline_qty")).alias("qty_generated"),
            (
                0.6 * pl.col("baseline_lead")
                + 0.4 * pl.coalesce([pl.col("total_lead_time_days"), pl.col("base_lead_time_days"), pl.col("baseline_lead")])
            ).alias("lead_generated"),
        )
        .select(
            [
                pl.col("date"),
                pl.col("item_id").cast(pl.Utf8),
                pl.col("material"),
                pl.col("familia"),
                pl.col("category"),
                pl.col("unidade_medida"),
                pl.col("deposito"),
                pl.col("site_id").cast(pl.Int64),
                pl.col("fornecedor"),
                pl.col("qty_generated")
                .round(3)
                .clip(0.0, None)
                .alias("quantidade"),
                pl.col("lead_generated").round(3).clip(0.0, None).alias("lead_time_days"),
                pl.lit("backfill_internal_enrichment").alias("source"),
                pl.lit(True).alias("is_backfill"),
                pl.lit(0.6).alias("backfill_confidence"),
                pl.col("demand_multiplier").alias("context_demand_multiplier"),
                pl.col("regional_demand_multiplier"),
                pl.col("new_component_demand_multiplier"),
                pl.col("old_component_demand_multiplier"),
            ]
        )
        .collect()
        .sort(["date", "item_id", "site_id"])
    )

    return backfill, actual_start


def _write_outputs(backfill: pl.DataFrame, actual_start: date) -> None:
    BACKFILL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    backfill.write_parquet(BACKFILL_OUTPUT)

    payload = validate_fact_backfill(backfill.to_pandas(), actual_start)
    payload["metadata"] = {"generated_at": datetime.utcnow().isoformat()}
    _write_validation_result("fact-backfill", payload)

    summary = {
        "rows": backfill.height,
        "date_start": backfill["date"].min().isoformat(),
        "date_end": backfill["date"].max().isoformat(),
        "items": int(backfill["item_id"].n_unique()),
        "sites": int(backfill["site_id"].n_unique()),
        "actual_start": actual_start.isoformat(),
    }
    summary_path = SUMMARY_DIR / "nova_corrente_backfill_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    backfill, actual_start = build_backfill()
    if backfill.is_empty():
        print("No backfill rows generated; nothing written.")
        return

    _write_outputs(backfill, actual_start)

    print(
        f"[backfill] generated {backfill.height:,} rows "
        f"from {backfill['date'].min().isoformat()} to {backfill['date'].max().isoformat()} "
        f"covering {backfill['item_id'].n_unique()} items and "
        f"{backfill['site_id'].n_unique()} sites."
    )
    print(f"[backfill] written to {BACKFILL_OUTPUT}")


if __name__ == "__main__":
    main()