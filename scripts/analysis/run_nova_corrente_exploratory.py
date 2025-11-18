"""Exploratory analytics for Nova Corrente demand forecasting data.

This script integrates the Nova Corrente fact table with key Brazilian
telecom contextual datasets to produce descriptive statistics and
correlation diagnostics that can guide prescriptive modelling.

Outputs:
    - data/outputs/analysis/nova_corrente_daily_summary.csv
    - data/outputs/analysis/nova_corrente_monthly_summary.csv
    - data/outputs/analysis/nova_corrente_correlation_daily.csv
    - data/outputs/analysis/nova_corrente_correlation_monthly.csv
    - docs/reports/NOVA_CORRENTE_EXPLORATORY_ANALYSIS.md

The script assumes pandas/numpy are available in the active environment.
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _ensure_output_dirs() -> tuple[Path, Path]:
    analysis_dir = PROJECT_ROOT / "data" / "outputs" / "analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)

    reports_dir = PROJECT_ROOT / "docs" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    return analysis_dir, reports_dir


def load_nova_corrente() -> pd.DataFrame:
    path = PROJECT_ROOT / "data" / "outputs" / "nova_corrente" / "nova_corrente_enriched.csv"
    df = pd.read_csv(
        path,
        parse_dates=[
            "date",
            "data_requisitada",
            "data_solicitado",
            "data_compra",
        ],
        dayfirst=False,
    )
    return df


def load_brazilian_demand_factors() -> pd.DataFrame:
    path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "brazilian_demand_factors"
        / "brazilian_demand_factors_structured.csv"
    )
    df = pd.read_csv(path, parse_dates=["date"])
    # Clip precipitation to remove synthetic negative placeholder values.
    if "precipitation_mm" in df.columns:
        df["precipitation_mm"] = df["precipitation_mm"].clip(lower=0)
    return df


def load_brazilian_operator_metrics() -> pd.DataFrame:
    path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "brazilian_operators_structured"
        / "brazilian_operators_market_structured.csv"
    )
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def load_brazilian_iot() -> pd.DataFrame:
    path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "brazilian_iot_structured"
        / "brazilian_iot_market_structured.csv"
    )
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def load_brazilian_fiber() -> pd.DataFrame:
    path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "brazilian_fiber_structured"
        / "brazilian_fiber_expansion_structured.csv"
    )
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def load_anatel_municipal() -> pd.DataFrame:
    path = PROJECT_ROOT / "data" / "raw" / "anatel_municipal" / "anatel_municipal_sample.csv"
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(dict(year=df["ano"], month=df["mes"], day=1)) + pd.offsets.MonthEnd(0)
    return df


def summarise_missingness(df: pd.DataFrame, id_columns: list[str] | None = None) -> pd.DataFrame:
    id_columns = id_columns or []
    cols = [c for c in df.columns if c not in id_columns]
    missing = (
        df[cols]
        .isna()
        .mean()
        .reset_index(name="missing_pct")
        .rename(columns={"index": "column"})
        .sort_values("missing_pct", ascending=False)
    )
    return missing


def build_daily_summary(nova: pd.DataFrame) -> pd.DataFrame:
    daily = (
        nova.groupby("date")
        .agg(
            total_quantity=("quantidade", "sum"),
            families_active=("familia", "nunique"),
            items_active=("item_id", "nunique"),
            suppliers_active=("fornecedor", "nunique"),
            avg_lead_time=("lead_time_days", "mean"),
            median_lead_time=("lead_time_days", "median"),
            std_lead_time=("lead_time_days", "std"),
        )
        .reset_index()
        .sort_values("date")
    )

    return daily


def build_family_summary(nova: pd.DataFrame) -> pd.DataFrame:
    family = (
        nova.groupby(["date", "familia"])
        .agg(
            total_quantity=("quantidade", "sum"),
            items_active=("item_id", "nunique"),
            suppliers_active=("fornecedor", "nunique"),
            avg_lead_time=("lead_time_days", "mean"),
        )
        .reset_index()
    )
    return family


def build_monthly_summary(daily_summary: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        daily_summary.set_index("date")
        .resample("ME")
        .agg(
            total_quantity=("total_quantity", "sum"),
            mean_daily_quantity=("total_quantity", "mean"),
            families_active=("families_active", "max"),
            items_active=("items_active", "max"),
            suppliers_active=("suppliers_active", "max"),
            avg_lead_time=("avg_lead_time", "mean"),
        )
        .reset_index()
    )
    return monthly


def integrate_daily_context(
    daily: pd.DataFrame,
    demand_factors: pd.DataFrame,
) -> pd.DataFrame:
    cols = [
        "date",
        "gdp_growth_rate",
        "inflation_rate",
        "exchange_rate_brl_usd",
        "temperature_avg_c",
        "precipitation_mm",
        "is_flood_risk",
        "is_drought",
        "is_holiday",
        "is_weekend",
        "demand_multiplier",
    ]
    demand_cols = [c for c in cols if c in demand_factors.columns]
    merged = daily.merge(demand_factors[demand_cols], on="date", how="left")
    return merged


def integrate_monthly_context(
    monthly: pd.DataFrame,
    operator_metrics: pd.DataFrame,
    iot_metrics: pd.DataFrame,
    municipal_stats: pd.DataFrame,
) -> pd.DataFrame:
    operator_monthly = (
        operator_metrics.groupby("date")
        .agg(
            total_subscribers=("subscribers_millions", "sum"),
            max_market_share=("market_share", "max"),
            market_concentration=("market_share", lambda s: float(np.square(s).sum())),
            avg_revenue_growth=("revenue_growth_rate", "mean"),
        )
        .reset_index()
    )

    iot_monthly = (
        iot_metrics.groupby("date")
        .agg(
            total_iot_connections=("iot_connections_millions", "sum"),
            sectors_reporting=("sector", "nunique"),
        )
        .reset_index()
    )

    municipal_monthly = (
        municipal_stats.groupby("date")
        .agg(
            total_accesses=("acessos", "sum"),
            operators_reporting=("operadora", "nunique"),
            technologies_reporting=("tecnologia", "nunique"),
        )
        .reset_index()
    )

    merged = monthly.merge(operator_monthly, on="date", how="left")
    merged = merged.merge(iot_monthly, on="date", how="left")
    merged = merged.merge(municipal_monthly, on="date", how="left")

    return merged


def integrate_quarterly_context(
    monthly_with_context: pd.DataFrame, fiber_metrics: pd.DataFrame
) -> pd.DataFrame:
    fiber_metrics = fiber_metrics.copy()
    fiber_metrics["quarter"] = fiber_metrics["date"].dt.to_period("Q")
    fiber_quarterly = (
        fiber_metrics.groupby(["quarter"])
        .agg(
            household_penetration_mean=("household_penetration", "mean"),
            household_penetration_max=("household_penetration", "max"),
            regions_reporting=("region", "nunique"),
        )
        .reset_index()
    )
    monthly_with_context = monthly_with_context.copy()
    monthly_with_context["quarter"] = monthly_with_context["date"].dt.to_period("Q")
    merged = monthly_with_context.merge(fiber_quarterly, on="quarter", how="left")
    return merged


def compute_correlations(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    available = [c for c in cols if c in df.columns]
    if not available:
        return pd.DataFrame()
    corr = df[available].dropna().corr().round(3)
    return corr


def build_report(
    *,
    analysis_dir: Path,
    reports_dir: Path,
    nova: pd.DataFrame,
    daily_summary: pd.DataFrame,
    monthly_summary: pd.DataFrame,
    daily_context: pd.DataFrame,
    monthly_context: pd.DataFrame,
    correlations_daily: pd.DataFrame,
    correlations_monthly: pd.DataFrame,
    missing_nova: pd.DataFrame,
) -> None:
    demand_desc = daily_summary["total_quantity"].describe(percentiles=[0.1, 0.5, 0.9]).round(2)
    lead_time_desc = daily_summary["avg_lead_time"].describe(percentiles=[0.1, 0.5, 0.9]).round(2)

    top_families = (
        nova.groupby("familia")
        .agg(total_quantity=("quantidade", "sum"))
        .sort_values("total_quantity", ascending=False)
        .head(5)
    )

    correlation_daily_json = (
        correlations_daily.to_json(orient="split") if not correlations_daily.empty else "{}"
    )
    correlation_monthly_json = (
        correlations_monthly.to_json(orient="split") if not correlations_monthly.empty else "{}"
    )

    (analysis_dir / "nova_corrente_correlation_daily.json").write_text(
        correlation_daily_json, encoding="utf-8"
    )
    (analysis_dir / "nova_corrente_correlation_monthly.json").write_text(
        correlation_monthly_json, encoding="utf-8"
    )

    sections = []

    sections.append(
        """## Nova Corrente Exploratory Diagnostics

### 1. Data Coverage
"""
    )

    span_days = (nova["date"].max() - nova["date"].min()).days
    sections.append(
        dedent(
            f"""
            - **Fact records**: {len(nova):,} rows across {nova['familia'].nunique()} families,
              {nova['item_id'].nunique()} items, and {nova['fornecedor'].nunique()} suppliers.
            - **Temporal range**: {nova['date'].min().date()} → {nova['date'].max().date()} ({span_days} days).
            - **Daily quantity (sum)** — mean: {demand_desc['mean']:.2f}, std: {demand_desc['std']:.2f},
              min: {demand_desc['min']:.2f}, 90th percentile: {demand_desc['90%']:.2f}.
            - **Average lead time (days)** — mean: {lead_time_desc['mean']:.2f},
              median: {lead_time_desc['50%']:.2f}, 90th percentile: {lead_time_desc['90%']:.2f}.
            - **Top families by total quantity**: {', '.join(top_families.index)}.
            """
        ).strip()
    )

    sections.append(
        """
### 2. Data Quality Observations
"""
    )

    sections.append("Top missingness (excluding identifiers):")
    sections.append(missing_nova.head(10).to_markdown(index=False))

    sections.append(
        """
### 3. Daily Relationships (Nova Corrente × Demand Factors)
"""
    )

    coverage_daily = daily_context[["gdp_growth_rate", "inflation_rate", "exchange_rate_brl_usd"]].notna().mean()
    sections.append(
        dedent(
            """
            - Daily demand joined with macro factors (GDP, inflation, FX), weather, and risk flags.
            - Effective coverage (non-null ratios):
            """
        ).strip()
    )
    sections.append(coverage_daily.round(2).to_frame("coverage").to_markdown())

    if not correlations_daily.empty:
        sections.append("Daily correlation matrix (excerpt):")
        sections.append(correlations_daily.head(10).to_markdown())
    else:
        sections.append("Daily correlation matrix could not be computed (insufficient overlapping data).")

    sections.append(
        """
### 4. Monthly Relationships (Nova Corrente × Operators × IoT × Municipal Accesses)
"""
    )

    coverage_monthly = monthly_context[[
        "total_subscribers",
        "total_iot_connections",
        "total_accesses",
        "household_penetration_mean",
    ]].notna().mean()

    sections.append("Monthly feature coverage:")
    sections.append(coverage_monthly.round(2).to_frame("coverage").to_markdown())

    if not correlations_monthly.empty:
        sections.append("Monthly correlation matrix (excerpt):")
        sections.append(correlations_monthly.head(10).to_markdown())
    else:
        sections.append("Monthly correlation matrix could not be computed (insufficient overlapping data).")

    sections.append(
        """
### 5. Key Insights & Next Actions

1. Extend external signals: macro factors present full coverage, but weather and regulatory flags remain sparse — prioritise ingestion backfill.
2. Operator metrics show concentration (HHI) trends; consider joining with supplier families to detect operator-driven demand signals.
3. Municipal accesses provide high-growth signals for 2023; parse full Anatel archives to unlock >24 months and reduce under-fitting.
4. Fiber penetration currently uses synthetic growth values; replace with true Anatel data to avoid misleading correlations.
5. Prepare feature store: persist merged daily/monthly tables for downstream prescriptive experiments (Croston/SBA, probabilistic models).
"""
    )

    report_path = reports_dir / "NOVA_CORRENTE_EXPLORATORY_ANALYSIS.md"
    report_path.write_text("\n\n".join(sections), encoding="utf-8")


def main() -> None:
    analysis_dir, reports_dir = _ensure_output_dirs()

    nova = load_nova_corrente()
    demand_factors = load_brazilian_demand_factors()
    operator_metrics = load_brazilian_operator_metrics()
    iot_metrics = load_brazilian_iot()
    fiber_metrics = load_brazilian_fiber()
    municipal_stats = load_anatel_municipal()

    daily_summary = build_daily_summary(nova)
    family_summary = build_family_summary(nova)
    monthly_summary = build_monthly_summary(daily_summary)

    daily_context = integrate_daily_context(daily_summary, demand_factors)
    monthly_context = integrate_monthly_context(
        monthly_summary, operator_metrics, iot_metrics, municipal_stats
    )
    monthly_context = integrate_quarterly_context(monthly_context, fiber_metrics)

    daily_corr_cols = [
        "total_quantity",
        "avg_lead_time",
        "families_active",
        "gdp_growth_rate",
        "inflation_rate",
        "exchange_rate_brl_usd",
        "temperature_avg_c",
        "precipitation_mm",
        "demand_multiplier",
    ]
    monthly_corr_cols = [
        "total_quantity",
        "mean_daily_quantity",
        "avg_lead_time",
        "total_subscribers",
        "max_market_share",
        "market_concentration",
        "total_iot_connections",
        "total_accesses",
        "household_penetration_mean",
    ]

    correlations_daily = compute_correlations(daily_context, daily_corr_cols)
    correlations_monthly = compute_correlations(monthly_context, monthly_corr_cols)

    missing_nova = summarise_missingness(
        nova,
        id_columns=[
            "date",
            "item_id",
            "familia",
            "material",
            "fornecedor",
            "solicitacao",
        ],
    )

    # Persist outputs
    daily_summary.to_csv(
        analysis_dir / "nova_corrente_daily_summary.csv", index=False, encoding="utf-8"
    )
    family_summary.to_csv(
        analysis_dir / "nova_corrente_family_daily.csv", index=False, encoding="utf-8"
    )
    monthly_summary.to_csv(
        analysis_dir / "nova_corrente_monthly_summary.csv", index=False, encoding="utf-8"
    )
    daily_context.to_csv(
        analysis_dir / "nova_corrente_daily_with_context.csv", index=False, encoding="utf-8"
    )
    monthly_context.to_csv(
        analysis_dir / "nova_corrente_monthly_with_context.csv", index=False, encoding="utf-8"
    )

    if not correlations_daily.empty:
        correlations_daily.to_csv(
            analysis_dir / "nova_corrente_correlation_daily.csv", encoding="utf-8"
        )
    if not correlations_monthly.empty:
        correlations_monthly.to_csv(
            analysis_dir / "nova_corrente_correlation_monthly.csv", encoding="utf-8"
        )

    build_report(
        analysis_dir=analysis_dir,
        reports_dir=reports_dir,
        nova=nova,
        daily_summary=daily_summary,
        monthly_summary=monthly_summary,
        daily_context=daily_context,
        monthly_context=monthly_context,
        correlations_daily=correlations_daily,
        correlations_monthly=correlations_monthly,
        missing_nova=missing_nova,
    )


if __name__ == "__main__":
    main()


