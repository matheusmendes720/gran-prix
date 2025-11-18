"""Prescriptive analytics for Nova Corrente demand forecasting.

This script consumes Nova Corrente enriched fact data and previously
curated Brazilian contextual datasets to compute per-family risk scores,
macro-driver sensitivities, and actionable recommendations.

Outputs:
    - data/outputs/analysis/nova_corrente_family_risk.csv
    - data/outputs/analysis/nova_corrente_family_macro_corr.csv
    - docs/reports/NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md
"""

from __future__ import annotations

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


def load_core_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    fact = pd.read_csv(
        PROJECT_ROOT / "data" / "outputs" / "nova_corrente" / "nova_corrente_enriched.csv",
        parse_dates=["date", "data_solicitado", "data_compra"],
    )
    demand_factors = pd.read_csv(
        PROJECT_ROOT
        / "data"
        / "raw"
        / "brazilian_demand_factors"
        / "brazilian_demand_factors_structured.csv",
        parse_dates=["date"],
    )
    demand_factors["precipitation_mm"] = demand_factors["precipitation_mm"].clip(lower=0)
    return fact, demand_factors


def compute_family_metrics(fact: pd.DataFrame) -> pd.DataFrame:
    fact = fact.copy()
    fact["lead_time_days"] = fact["lead_time_days"].astype(float)

    family_daily = (
        fact.groupby(["date", "familia"], as_index=False)
        .agg(
            total_quantity=("quantidade", "sum"),
            avg_lead_time=("lead_time_days", "mean"),
            high_lead_time_ratio=("lead_time_days", lambda s: float((s > 21).mean())),
            records=("item_id", "count"),
        )
    )

    family_metrics = (
        family_daily.groupby("familia")
        .agg(
            days_observed=("date", "nunique"),
            total_quantity=("total_quantity", "sum"),
            mean_daily_quantity=("total_quantity", "mean"),
            std_daily_quantity=("total_quantity", "std"),
            coefficient_variation=("total_quantity", lambda s: float(np.nanstd(s) / (np.nanmean(s) + 1e-9))),
            avg_lead_time=("avg_lead_time", "mean"),
            median_lead_time=("avg_lead_time", "median"),
            high_lead_time_ratio=("high_lead_time_ratio", "mean"),
            records=("records", "sum"),
        )
        .reset_index()
    )

    family_metrics["coefficient_variation"] = family_metrics["coefficient_variation"].replace(
        [np.inf, -np.inf], np.nan
    )
    return family_metrics, family_daily


def compute_macro_correlations(
    family_daily: pd.DataFrame, demand_factors: pd.DataFrame
) -> pd.DataFrame:
    merged = family_daily.merge(demand_factors, on="date", how="left")
    macro_cols = [
        "gdp_growth_rate",
        "inflation_rate",
        "exchange_rate_brl_usd",
        "temperature_avg_c",
        "precipitation_mm",
        "demand_multiplier",
    ]

    results = []
    for familia, group in merged.groupby("familia"):
        available_cols = [c for c in macro_cols if group[c].notna().sum() >= 10]
        if not available_cols:
            continue
        subset = group[["total_quantity", *available_cols]].dropna()
        if len(subset) < 10:
            continue
        corrs = subset.corr().loc["total_quantity", available_cols]
        results.append({"familia": familia, **corrs.to_dict(), "n_obs": len(subset)})

    if not results:
        return pd.DataFrame(columns=["familia", "n_obs", *macro_cols])

    out = pd.DataFrame(results)
    return out


def compute_risk_scores(
    family_metrics: pd.DataFrame, macro_corr: pd.DataFrame
) -> pd.DataFrame:
    df = family_metrics.merge(macro_corr, on="familia", how="left", suffixes=('', '_macro'))

    # Normalize metrics for scoring.
    def normalize(series: pd.Series) -> pd.Series:
        series = series.astype(float)
        return (series - series.min()) / (series.max() - series.min() + 1e-9)

    df["cv_score"] = normalize(df["coefficient_variation"].fillna(df["coefficient_variation"].median()))
    df["lead_time_score"] = normalize(df["avg_lead_time"].fillna(df["avg_lead_time"].median()))
    df["high_lead_time_score"] = normalize(df["high_lead_time_ratio"].fillna(0))

    macro_abs_cols = [
        c
        for c in [
            "gdp_growth_rate",
            "inflation_rate",
            "exchange_rate_brl_usd",
            "temperature_avg_c",
            "precipitation_mm",
            "demand_multiplier",
        ]
        if c in df.columns
    ]

    if macro_abs_cols:
        df["macro_sensitivity"] = df[macro_abs_cols].abs().max(axis=1)
        df["macro_score"] = normalize(df["macro_sensitivity"].fillna(0))
    else:
        df["macro_score"] = 0

    df["composite_risk"] = (
        0.4 * df["cv_score"]
        + 0.3 * df["lead_time_score"]
        + 0.2 * df["high_lead_time_score"]
        + 0.1 * df.get("macro_score", 0)
    )

    df = df.sort_values("composite_risk", ascending=False)
    return df


def build_recommendations(df: pd.DataFrame) -> list[str]:
    recommendations = []
    high_risk = df.head(5)
    for _, row in high_risk.iterrows():
        bullets = []
        if row["coefficient_variation"] > 1.0:
            bullets.append("• High demand volatility — implement dynamic safety stock and monitor weekly.")
        if row["avg_lead_time"] >= 15:
            bullets.append("• Lead time above 15 days — negotiate faster supplier SLAs or pre-stage inventory.")
        if row.get("macro_sensitivity", 0) > 0.4:
            bullets.append("• Demand tied to macro factors — link forecasts to GDP/FX scenarios.")
        if row["high_lead_time_ratio"] > 0.3:
            bullets.append("• >30% orders exceed 3-week lead time — escalate procurement priorities.")
        if not bullets:
            bullets.append("• Monitor routinely; risk drivers within acceptable bounds.")
        msg = dedent(
            f"""
            #### {row['familia']}
            - Composite risk: {row['composite_risk']:.2f}
            - Demand CV: {row['coefficient_variation']:.2f} | Avg lead time: {row['avg_lead_time']:.2f} days
            - High lead ratio: {row['high_lead_time_ratio']:.2%} | Records analysed: {int(row['records'])}
            """.strip()
        )
        recommendations.append(msg)
        recommendations.extend(bullets)
        recommendations.append("")

    return recommendations


def write_prescriptive_report(
    *,
    reports_dir: Path,
    risk_df: pd.DataFrame,
    macro_corr: pd.DataFrame,
    recommendations: list[str],
) -> None:
    top_missing_macro = macro_corr.sort_values("n_obs", ascending=False).tail(5)

    sections = ["## Nova Corrente Prescriptive Brief"]

    sections.append(
        dedent(
            f"""
            ### 1. Risk Ranking Overview

            | Family | Composite Risk | Demand CV | Avg Lead Time (d) | High Lead Ratio |
            |--------|----------------|-----------|-------------------|-----------------|
            {risk_df[['familia','composite_risk','coefficient_variation','avg_lead_time','high_lead_time_ratio']].head(10).to_markdown(index=False)}
            """
        ).strip()
    )

    sections.append("### 2. Macro Sensitivity Coverage")
    if not macro_corr.empty:
        sections.append(macro_corr.sort_values("n_obs", ascending=False).head(10).to_markdown(index=False))
    else:
        sections.append("Macro correlation coverage insufficient (<10 overlapping datapoints). Prioritise enrichment backfill.")

    sections.append("### 3. Targeted Recommendations")
    sections.extend(recommendations or ["- No high-risk families identified; maintain baseline controls."])

    sections.append(
        "### 4. Data Gaps & Next Actions\n\n"
        "- Expand macro/weather coverage: less than 25 overlapping daily points for most families.\n"
        "- Parse full Anatel municipal/broadband datasets to extend lead-time history beyond 12 months.\n"
        "- Replace placeholder fiber growth values before using in scenario simulations.\n"
        "- Promote a feature store to persist daily family metrics for Croston/SBA modelling." 
    )

    (reports_dir / "NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md").write_text(
        "\n\n".join(sections), encoding="utf-8"
    )


def main() -> None:
    analysis_dir, reports_dir = _ensure_output_dirs()
    fact, demand_factors = load_core_data()
    family_metrics, family_daily = compute_family_metrics(fact)
    macro_corr = compute_macro_correlations(family_daily, demand_factors)
    risk_df = compute_risk_scores(family_metrics, macro_corr)
    recommendations = build_recommendations(risk_df)

    risk_df.to_csv(analysis_dir / "nova_corrente_family_risk.csv", index=False, encoding="utf-8")
    macro_corr.to_csv(analysis_dir / "nova_corrente_family_macro_corr.csv", index=False, encoding="utf-8")

    write_prescriptive_report(
        reports_dir=reports_dir,
        risk_df=risk_df,
        macro_corr=macro_corr,
        recommendations=recommendations,
    )


if __name__ == "__main__":
    main()


