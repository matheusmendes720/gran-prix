"""
Build feature store datasets from Silver-level external tables.

The output is stored under ``data/feature_store/external/`` and focuses on a
daily macro + climate dataframe aligned with Nova Corrente's timelines.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


SILVER_ROOT = Path("data/silver/external_factors")
FEATURE_ROOT = Path("data/feature_store/external")
START_DATE = pd.Timestamp("2021-01-01")


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


def build_macro_features() -> pd.DataFrame:
    selic = load_parquet(SILVER_ROOT / "macro" / "selic_daily.parquet")
    ptax = load_parquet(SILVER_ROOT / "macro" / "ptax_rates.parquet")
    ipca = load_parquet(SILVER_ROOT / "macro" / "ipca_monthly.parquet")
    ipca15 = load_parquet(SILVER_ROOT / "macro" / "ipca15_monthly.parquet")
    inpc = load_parquet(SILVER_ROOT / "macro" / "inpc_monthly.parquet")
    unemployment = load_parquet(SILVER_ROOT / "macro" / "unemployment_rate.parquet")
    pib_quarterly = load_parquet(SILVER_ROOT / "macro" / "pib_quarterly_yoy.parquet")
    pib_annual = load_parquet(SILVER_ROOT / "macro" / "pib_annual_value.parquet")
    cds_spread = load_parquet(SILVER_ROOT / "macro" / "cds_spread.parquet")
    ppp_factor = load_parquet(SILVER_ROOT / "macro" / "ppp_conversion_factor.parquet")

    if selic.empty or ptax.empty or ipca.empty:
        return pd.DataFrame()

    selic = selic.rename(columns={"date": "date"})
    selic["date"] = pd.to_datetime(selic["date"])
    selic = selic[selic["date"] >= START_DATE]
    selic = selic.drop(columns=["run_date"], errors="ignore")
    if "selic" in selic.columns:
        selic["selic"] = pd.to_numeric(selic["selic"], errors="coerce")
    elif "selic_rate" in selic.columns:
        selic["selic"] = pd.to_numeric(selic["selic_rate"], errors="coerce")
    else:
        return pd.DataFrame()

    ptax = ptax.copy()
    ptax["date"] = pd.to_datetime(ptax["date"])
    ptax = ptax[ptax["date"] >= START_DATE]
    for col in ("buy_rate", "sell_rate", "parity_buy", "parity_sell"):
        if col in ptax.columns:
            ptax[col] = pd.to_numeric(ptax[col], errors="coerce")

    ptax_daily = (
        ptax.groupby(["date", "currency"], as_index=False)["sell_rate"].mean()
        if "sell_rate" in ptax.columns
        else pd.DataFrame()
    )

    if not ptax_daily.empty:
        ptax_pivot = ptax_daily.pivot(index="date", columns="currency", values="sell_rate")
        ptax_pivot = ptax_pivot.rename(
            columns={
                "USD": "usd_brl",
                "EUR": "eur_brl",
                "CNY": "cny_brl",
            }
        )
    else:
        ptax_pivot = pd.DataFrame()

    ipca = ipca.rename(columns={"period": "date", "ipca": "ipca_mom"})
    ipca["date"] = pd.to_datetime(ipca["date"])
    ipca = ipca[ipca["date"] >= START_DATE]
    ipca = ipca.drop(columns=["run_date"], errors="ignore")
    ipca.set_index("date", inplace=True)
    ipca_daily = ipca.resample("D").ffill()

    ipca15_daily = pd.DataFrame()
    if not ipca15.empty:
        ipca15 = ipca15.rename(columns={"period": "date", "ipca15": "ipca15_mom"})
        ipca15["date"] = pd.to_datetime(ipca15["date"])
        ipca15 = ipca15[ipca15["date"] >= START_DATE]
        ipca15 = ipca15.drop(columns=["run_date"], errors="ignore")
        ipca15_daily = (
            ipca15.set_index("date")
            .resample("D")
            .ffill()
        )

    inpc_daily = pd.DataFrame()
    if not inpc.empty:
        inpc = inpc.rename(columns={"period": "date", "inpc": "inpc_mom"})
        inpc["date"] = pd.to_datetime(inpc["date"])
        inpc = inpc[inpc["date"] >= START_DATE]
        inpc = inpc.drop(columns=["run_date"], errors="ignore")
        inpc_daily = (
            inpc.set_index("date")
            .resample("D")
            .ffill()
        )

    unemployment_daily = pd.DataFrame()
    if not unemployment.empty:
        unemployment = unemployment.rename(columns={"period": "date", "unemployment_rate": "unemployment_rate"})
        unemployment["date"] = pd.to_datetime(unemployment["date"])
        unemployment = unemployment[unemployment["date"] >= START_DATE]
        unemployment = unemployment.drop(columns=["run_date"], errors="ignore")
        unemployment_daily = (
            unemployment.set_index("date")
            .resample("D")
            .ffill()
        )

    pib_quarterly_daily = pd.DataFrame()
    if not pib_quarterly.empty:
        pib_quarterly = pib_quarterly.rename(columns={"period": "date"})
        pib_quarterly["date"] = pd.to_datetime(pib_quarterly["date"])
        pib_quarterly = pib_quarterly.drop(columns=["run_date"], errors="ignore")
        pib_quarterly_daily = (
            pib_quarterly.set_index("date")
            .resample("D")
            .ffill()
        )

    pib_annual_daily = pd.DataFrame()
    if not pib_annual.empty:
        pib_annual = pib_annual.rename(columns={"period": "date"})
        pib_annual["date"] = pd.to_datetime(pib_annual["date"])
        pib_annual = pib_annual.drop(columns=["run_date"], errors="ignore")
        pib_annual_daily = (
            pib_annual.set_index("date")
            .resample("D")
            .ffill()
        )

    cds_daily = pd.DataFrame()
    if not cds_spread.empty:
        cds_spread = cds_spread.rename(columns={"date": "date"})
        cds_spread["date"] = pd.to_datetime(cds_spread["date"])
        cds_spread = cds_spread[cds_spread["date"] >= START_DATE]
        cds_daily = (
            cds_spread.set_index("date")
            .resample("D")
            .ffill()
        )
        cds_daily = cds_daily.reset_index().drop(columns=["run_date"], errors="ignore")

    ppp_daily = pd.DataFrame()
    if not ppp_factor.empty:
        ppp_factor = ppp_factor.rename(columns={"date": "date"})
        ppp_factor["date"] = pd.to_datetime(ppp_factor["date"])
        ppp_daily = (
            ppp_factor.set_index("date")
            .resample("D")
            .ffill()
        )
        ppp_daily = ppp_daily.reset_index().drop(columns=["run_date"], errors="ignore")

    df = (
        selic.set_index("date")
        .join(ptax_pivot, how="left")
        .join(ipca_daily, how="left")
        .sort_index()
        .ffill()
        .reset_index()
    )

    if not ipca15_daily.empty:
        df = df.merge(ipca15_daily.reset_index(), on="date", how="left")
    if not inpc_daily.empty:
        df = df.merge(inpc_daily.reset_index(), on="date", how="left")
    if not unemployment_daily.empty:
        df = df.merge(unemployment_daily.reset_index(), on="date", how="left")
    if not pib_quarterly_daily.empty:
        df = df.merge(pib_quarterly_daily.reset_index(), on="date", how="left")
    if not pib_annual_daily.empty:
        df = df.merge(pib_annual_daily.reset_index(), on="date", how="left")
    if not cds_daily.empty:
        df = df.merge(cds_daily, on="date", how="left")
    if not ppp_daily.empty:
        df = df.merge(ppp_daily, on="date", how="left")

    df.sort_values("date", inplace=True)
    return df


def build_climate_features(city: str = "salvador_ba") -> pd.DataFrame:
    climate = load_parquet(SILVER_ROOT / "climatic" / "openmeteo_daily.parquet")
    if climate.empty:
        return pd.DataFrame()

    climate = climate[climate["city"] == city].copy()
    climate["date"] = pd.to_datetime(climate["date"])
    climate = climate[climate["date"] >= START_DATE]
    climate.sort_values("date", inplace=True)
    climate = climate.rename(
        columns={
            "temperature_2m_daily": "temperature_c",
            "relative_humidity_2m_daily": "humidity_percent",
            "precipitation_daily": "precipitation_mm",
            "wind_speed_10m_daily": "wind_speed_kmh",
        }
    )
    return climate[["date", "temperature_c", "humidity_percent", "precipitation_mm", "wind_speed_kmh"]]


def load_fuel_features() -> pd.DataFrame:
    fuel = load_parquet(SILVER_ROOT / "logistics" / "anp_fuel_daily.parquet")
    if fuel.empty:
        return pd.DataFrame()
    fuel["date"] = pd.to_datetime(fuel["date"])
    fuel = fuel[fuel["date"] >= START_DATE]
    fuel.sort_values("date", inplace=True)
    return fuel


def load_freight_features() -> pd.DataFrame:
    freight = load_parquet(SILVER_ROOT / "logistics" / "freight_worldbank.parquet")
    if freight.empty:
        return pd.DataFrame()
    freight["date"] = pd.to_datetime(freight["date"])
    freight = freight[freight["date"] >= START_DATE]
    freight.sort_values("date", inplace=True)
    freight = (
        freight.set_index("date")
        .resample("D")
        .ffill()
        .reset_index()
    )
    return freight


def load_baltic_dry_features() -> pd.DataFrame:
    baltic = load_parquet(SILVER_ROOT / "logistics" / "baltic_dry.parquet")
    if baltic.empty:
        return pd.DataFrame()
    baltic["date"] = pd.to_datetime(baltic["date"])
    baltic = baltic[baltic["date"] >= START_DATE]
    baltic.sort_values("date", inplace=True)
    baltic = (
        baltic.set_index("date")
        .resample("D")
        .ffill()
        .reset_index()
    )
    return baltic


def load_freightos_features() -> pd.DataFrame:
    fbx = load_parquet(SILVER_ROOT / "logistics" / "freightos_fbx.parquet")
    if fbx.empty:
        return pd.DataFrame()
    fbx["date"] = pd.to_datetime(fbx["date"])
    fbx = fbx[fbx["date"] >= START_DATE]
    fbx.sort_values("date", inplace=True)
    fbx = (
        fbx.set_index("date")
        .resample("D")
        .ffill()
        .reset_index()
    )
    return fbx


def load_drewry_features() -> pd.DataFrame:
    drewry = load_parquet(SILVER_ROOT / "logistics" / "drewry_wci.parquet")
    if drewry.empty:
        return pd.DataFrame()
    drewry["date"] = pd.to_datetime(drewry["date"])
    drewry = drewry[drewry["date"] >= START_DATE]
    drewry.sort_values("date", inplace=True)
    drewry = (
        drewry.set_index("date")
        .resample("D")
        .ffill()
        .reset_index()
    )
    return drewry


def load_antt_features() -> pd.DataFrame:
    antt = load_parquet(SILVER_ROOT / "logistics" / "antt_metrics.parquet")
    if antt.empty:
        return pd.DataFrame()
    antt["date"] = pd.to_datetime(antt["date"])
    antt = antt[antt["date"] >= START_DATE]
    antt.sort_values("date", inplace=True)
    antt = (
        antt.set_index("date")
        .resample("D")
        .ffill()
        .reset_index()
    )
    return antt


def build_macro_climate_features() -> pd.DataFrame:
    macro = build_macro_features()
    climate = build_climate_features()
    fuel = load_fuel_features()
    freight = load_freight_features()
    baltic = load_baltic_dry_features()
    fbx = load_freightos_features()
    drewry = load_drewry_features()
    antt = load_antt_features()
    if macro.empty:
        return pd.DataFrame()
    starts = [START_DATE]
    if not climate.empty:
        starts.append(climate["date"].min())
    if not fuel.empty:
        starts.append(fuel["date"].min())
    if not freight.empty:
        starts.append(freight["date"].min())
    if not baltic.empty:
        starts.append(baltic["date"].min())
    if not fbx.empty:
        starts.append(fbx["date"].min())
    if not drewry.empty:
        starts.append(drewry["date"].min())
    if not antt.empty:
        starts.append(antt["date"].min())
    overall_start = max(starts)
    macro = macro[macro["date"] >= overall_start]

    merged = macro
    if not climate.empty:
        merged = merged.merge(climate, on="date", how="left")
    if not fuel.empty:
        merged = merged.merge(fuel, on="date", how="left")
        fuel_cols = [col for col in fuel.columns if col != "date"]
        merged[fuel_cols] = merged[fuel_cols].ffill()
    if not freight.empty:
        merged = merged.merge(freight, on="date", how="left")
        freight_cols = [col for col in freight.columns if col != "date"]
        merged[freight_cols] = merged[freight_cols].ffill()
    if not baltic.empty:
        merged = merged.merge(baltic, on="date", how="left")
        merged["baltic_dry_index"] = merged["baltic_dry_index"].ffill()
    if not fbx.empty:
        merged = merged.merge(fbx, on="date", how="left")
        merged["freightos_fbx"] = merged["freightos_fbx"].ffill()
    if not drewry.empty:
        merged = merged.merge(drewry, on="date", how="left")
        merged["drewry_wci"] = merged["drewry_wci"].ffill()
    if not antt.empty:
        merged = merged.merge(antt, on="date", how="left")
        antt_cols = [col for col in antt.columns if col != "date"]
        merged[antt_cols] = merged[antt_cols].ffill()

    merged = enrich_feature_space(merged)
    return merged


def enrich_feature_space(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.sort_values("date").reset_index(drop=True)

    # Rolling statistics for diesel prices
    for col in ["diesel_price", "diesel_s10_price"]:
        if col in df:
            df[f"{col}_ma7"] = df[col].rolling(window=7, min_periods=1).mean()
            df[f"{col}_ma30"] = df[col].rolling(window=30, min_periods=1).mean()
            df[f"{col}_volatility_30"] = df[col].rolling(window=30, min_periods=5).std()

    # Baltic Dry Index momentum features
    if "baltic_dry_index" in df:
        df["baltic_dry_index_ma7"] = df["baltic_dry_index"].rolling(7, min_periods=1).mean()
        df["baltic_dry_index_ma30"] = df["baltic_dry_index"].rolling(30, min_periods=1).mean()
        df["baltic_dry_index_pct_change_7d"] = (
            df["baltic_dry_index"].pct_change(periods=7).replace([np.inf, -np.inf], np.nan)
        )
        df["baltic_dry_index_pct_change_30d"] = (
            df["baltic_dry_index"].pct_change(periods=30).replace([np.inf, -np.inf], np.nan)
        )
        zscore_window = df["baltic_dry_index"].rolling(window=90, min_periods=10)
        df["baltic_dry_index_zscore_90d"] = (
            (df["baltic_dry_index"] - zscore_window.mean()) / zscore_window.std()
        )

    # Interaction features between fuel and freight
    if {"diesel_price", "baltic_dry_index"}.issubset(df.columns):
        df["diesel_vs_baltic_ratio"] = df["diesel_price"] / df["baltic_dry_index"]
        df["diesel_baltic_spread"] = df["diesel_price"] - (df["baltic_dry_index"] / 100.0)

    if {"diesel_s10_price", "air_freight_mtkm_wld"}.issubset(df.columns):
        df["diesel_s10_x_airfreight"] = df["diesel_s10_price"] * df["air_freight_mtkm_wld"]

    if {"diesel_price", "container_port_traffic_teu_wld"}.issubset(df.columns):
        df["diesel_x_container_traffic"] = (
            df["diesel_price"] * df["container_port_traffic_teu_wld"]
        )

    if "freightos_fbx" in df:
        df["freightos_fbx_ma7"] = df["freightos_fbx"].rolling(7, min_periods=1).mean()
        df["freightos_fbx_ma30"] = df["freightos_fbx"].rolling(30, min_periods=1).mean()
        df["freightos_fbx_pct_change_7d"] = (
            df["freightos_fbx"].pct_change(periods=7).replace([np.inf, -np.inf], np.nan)
        )

    if "drewry_wci" in df:
        df["drewry_wci_ma7"] = df["drewry_wci"].rolling(7, min_periods=1).mean()
        df["drewry_wci_ma30"] = df["drewry_wci"].rolling(30, min_periods=1).mean()
        df["drewry_wci_pct_change_7d"] = (
            df["drewry_wci"].pct_change(periods=7).replace([np.inf, -np.inf], np.nan)
        )

    if {"freightos_fbx", "drewry_wci"}.issubset(df.columns):
        df["fbx_wci_spread"] = df["freightos_fbx"] - df["drewry_wci"]

    if {"freightos_fbx", "baltic_dry_index"}.issubset(df.columns):
        df["fbx_to_baltic_ratio"] = df["freightos_fbx"] / df["baltic_dry_index"]

    # ANTT logistics rolling summaries
    antt_cols = [col for col in df.columns if col.startswith("antt_")]
    for col in antt_cols:
        df[f"{col}_ma7"] = df[col].rolling(7, min_periods=1).mean()
        df[f"{col}_ma30"] = df[col].rolling(30, min_periods=1).mean()
        df[f"{col}_pct_change_14d"] = (
            df[col].pct_change(periods=14).replace([np.inf, -np.inf], np.nan)
        )

    if antt_cols:
        rolling_mean = df[antt_cols].rolling(90, min_periods=15).mean()
        rolling_std = df[antt_cols].rolling(90, min_periods=15).std().replace(0, np.nan)
        zscores = (df[antt_cols] - rolling_mean) / rolling_std
        df["antt_logistics_stress_index"] = zscores.mean(axis=1)
        df["antt_capacity_utilization_proxy"] = df[antt_cols].mean(axis=1)
        if "diesel_price" in df.columns:
            denominator = df[antt_cols].mean(axis=1).replace(0, np.nan)
            df["diesel_vs_antt_stress"] = df["diesel_price"] / denominator
        if "baltic_dry_index" in df.columns:
            denominator = df[antt_cols].mean(axis=1).replace(0, np.nan)
            df["baltic_vs_antt_spread"] = df["baltic_dry_index"] - denominator

    if "cds_spread_bps" in df:
        df["cds_spread_bps_ma7"] = df["cds_spread_bps"].rolling(7, min_periods=1).mean()
        df["cds_spread_bps_ma30"] = df["cds_spread_bps"].rolling(30, min_periods=1).mean()
        df["cds_spread_bps_pct_change_30d"] = (
            df["cds_spread_bps"].pct_change(periods=30).replace([np.inf, -np.inf], np.nan)
        )

    if "ppp_conversion_factor" in df:
        df["ppp_conversion_factor_yoy"] = (
            df["ppp_conversion_factor"].pct_change(periods=365).replace([np.inf, -np.inf], np.nan)
        )

    # Fill any remaining gaps created by calculations
    engineered_cols = [
        col
        for col in df.columns
        if col.endswith(
            (
                "_ma7",
                "_ma30",
                "_volatility_30",
                "_pct_change_7d",
                "_pct_change_14d",
                "_pct_change_30d",
                "_zscore_90d",
                "_yoy",
            )
        )
        or col in {
            "diesel_vs_baltic_ratio",
            "diesel_baltic_spread",
            "diesel_s10_x_airfreight",
            "diesel_x_container_traffic",
            "fbx_wci_spread",
            "fbx_to_baltic_ratio",
            "antt_logistics_stress_index",
            "antt_capacity_utilization_proxy",
            "diesel_vs_antt_stress",
            "baltic_vs_antt_spread",
            "ppp_conversion_factor_yoy",
        }
    ]

    engineered = df[engineered_cols].replace([np.inf, -np.inf], np.nan)
    engineered = engineered.ffill().bfill()
    df[engineered_cols] = engineered

    return df


def main() -> None:
    ensure_directory(FEATURE_ROOT)
    macro_climate = build_macro_climate_features()
    if macro_climate.empty:
        print("No feature data generated.")
        return
    output_path = FEATURE_ROOT / "macro_climate_daily.parquet"
    macro_climate.to_parquet(output_path, index=False)
    print(f"Wrote feature dataset with {len(macro_climate)} rows to {output_path}")


if __name__ == "__main__":
    main()

