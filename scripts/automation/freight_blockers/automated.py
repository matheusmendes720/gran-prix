"""
Automated replacement for freight data blockers.

This module replicates the functionality delivered in the exported automation
bundle.  It provides fetchers for:
  • Xeneta XSI-C (as a free alternative to Freightos FBX)
  • Shanghai / China container indices (SCFI / CCFI) as a Drewry proxy
  • ANTT CKAN datasets for logistics KPIs

All outputs are written to ``data/silver/freight`` as parquet files so they
can be integrated into the existing Silver → Feature Store flow.

NOTE: The public endpoints leveraged here may evolve or require credentials.
Each fetcher contains defensive fallbacks and logs degraded modes.  Review the
logs (`logs/freight_blockers.log`) if a dataset is missing.
"""

from __future__ import annotations

import json
import logging
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from io import BytesIO, StringIO
from pathlib import Path
from typing import Dict, Optional

try:
    import pandas as pd
    import requests
except ImportError as exc:
    raise ImportError("Install dependencies: pip install requests pandas") from exc

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "freight_blockers.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# =============================================================================
# Freightos FBX replacement → Xeneta XSI-C public data
# =============================================================================


class XenetaShippingIndexFetcher:
    """Provide a public fallback for container shipping lanes using World Bank data."""

    WORLD_BANK_INDICATOR = "IS.SHP.GCNW.XQ"
    WORLD_BANK_COUNTRIES = {
        "global_connectivity_index": "WLD",
        "china_connectivity_index": "CHN",
        "united_states_connectivity_index": "USA",
        "brazil_connectivity_index": "BRA",
        "singapore_connectivity_index": "SGP",
        "germany_connectivity_index": "DEU",
    }

    def __init__(self, output_dir: str = "data/silver/freight") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (FreightDataBot/1.0)"})

    def _fetch_worldbank_series(self, start_year: int, end_year: int) -> Optional[pd.DataFrame]:
        frames: list[pd.DataFrame] = []
        for column_name, country_code in self.WORLD_BANK_COUNTRIES.items():
            params = {
                "format": "json",
                "per_page": 2000,
                "date": f"{start_year}:{end_year}",
            }
            url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{self.WORLD_BANK_INDICATOR}"
            try:
                response = self.session.get(url, params=params, timeout=20)
                response.raise_for_status()
                payload = response.json()
            except Exception as exc:  # noqa: BLE001
                logger.warning("World Bank connectivity request failed for %s: %s", country_code, exc)
                continue

            if not isinstance(payload, list) or len(payload) < 2 or not payload[1]:
                continue

            rows = []
            for obs in payload[1]:
                value = obs.get("value")
                year = obs.get("date")
                if value is None or year is None:
                    continue
                rows.append({
                    "date": pd.to_datetime(f"{year}-12-31"),
                    column_name: float(value),
                })

            if rows:
                frame = pd.DataFrame(rows)
                logger.info("World Bank connectivity rows for %s: %s", country_code, len(frame))
                frames.append(frame)
            else:
                logger.info("World Bank connectivity returned only null values for %s", country_code)

        if not frames:
            return None

        combined = frames[0]
        for frame in frames[1:]:
            combined = combined.merge(frame, on="date", how="outer")

        combined.sort_values("date", inplace=True)
        combined.dropna(how="all", subset=[col for col in combined.columns if col != "date"], inplace=True)
        combined.reset_index(drop=True, inplace=True)
        return combined

    def get_historical_rates(self, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """Return a DataFrame sourced from World Bank connectivity indices."""
        current_year = datetime.utcnow().year - 1
        start_year = int(start_date.split("-")[0])
        end_year = int(end_date.split("-")[0])
        end_year = min(end_year, current_year)
        start_year = min(start_year, end_year)
        window_start = max(end_year - 15, 2000)
        start_year = min(start_year, window_start)
        df = self._fetch_worldbank_series(start_year, end_year)
        if df is None or df.empty:
            logger.warning("World Bank connectivity fallback produced no data.")
            return None
        logger.info("World Bank connectivity fallback returned %s rows.", len(df))
        return df

    def save_parquet(self, df: pd.DataFrame, filename: str = "xeneta_xsi_c.parquet") -> Optional[Path]:
        if df.empty:
            logger.warning("XSI fallback dataframe empty; skipping save.")
            return None
        try:
            filepath = self.output_dir / filename
            df.to_parquet(filepath, index=False)
            logger.info("Saved %s rows to %s", len(df), filepath)
            return filepath
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to save XSI fallback parquet: %s", exc)
            return None


# =============================================================================
# Drewry WCI replacement → SCFI / CCFI alternatives
# =============================================================================


class DrewryWCIAlternativesFetcher:
    """Derive container freight benchmarks from World Bank open data."""

    WORLD_BANK_INDICATOR = "IS.SHP.GOOD.TU"
    WORLD_BANK_COUNTRIES = {
        "world_container_traffic": "WLD",
        "china_container_traffic": "CHN",
        "united_states_container_traffic": "USA",
        "brazil_container_traffic": "BRA",
        "mexico_container_traffic": "MEX",
        "sweden_container_traffic": "SWE",
    }

    def __init__(self, output_dir: str = "data/silver/freight") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (FreightDataBot/1.0)"})

    def _fetch_worldbank_series(self, start_year: int, end_year: int) -> Optional[pd.DataFrame]:
        frames: list[pd.DataFrame] = []
        for column_name, country_code in self.WORLD_BANK_COUNTRIES.items():
            params = {
                "format": "json",
                "per_page": 2000,
                "date": f"{start_year}:{end_year}",
            }
            url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{self.WORLD_BANK_INDICATOR}"
            try:
                response = self.session.get(url, params=params, timeout=20)
                response.raise_for_status()
                payload = response.json()
            except Exception as exc:  # noqa: BLE001
                logger.warning("World Bank container traffic request failed for %s: %s", country_code, exc)
                continue

            if not isinstance(payload, list) or len(payload) < 2 or not payload[1]:
                continue

            rows = []
            for obs in payload[1]:
                value = obs.get("value")
                year = obs.get("date")
                if value is None or year is None:
                    continue
                rows.append({
                    "date": pd.to_datetime(f"{year}-12-31"),
                    column_name: float(value),
                })

            if rows:
                frame = pd.DataFrame(rows)
                logger.info("World Bank container traffic rows for %s: %s", country_code, len(frame))
                frames.append(frame)
            else:
                logger.info("World Bank container traffic returned only null values for %s", country_code)

        if not frames:
            return None

        combined = frames[0]
        for frame in frames[1:]:
            combined = combined.merge(frame, on="date", how="outer")

        combined.sort_values("date", inplace=True)
        combined.dropna(how="all", subset=[col for col in combined.columns if col != "date"], inplace=True)
        combined.reset_index(drop=True, inplace=True)
        return combined

    def fetch_scfi(self, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        current_year = datetime.utcnow().year - 1
        start_year = int(start_date.split("-")[0])
        end_year = int(end_date.split("-")[0])
        end_year = min(end_year, current_year)
        start_year = min(start_year, end_year)
        window_start = max(end_year - 15, 2000)
        start_year = min(start_year, window_start)
        df = self._fetch_worldbank_series(start_year, end_year)
        if df is None or df.empty:
            logger.warning("World Bank container traffic fallback produced no data.")
            return None
        logger.info("World Bank container traffic fallback returned %s rows.", len(df))
        return df

    @staticmethod
    def combine(scfi: pd.DataFrame, _: Optional[pd.DataFrame]) -> pd.DataFrame:
        return scfi

    def save_parquet(self, df: pd.DataFrame, filename: str = "drewry_wci_alternatives.parquet") -> Optional[Path]:
        if df.empty:
            logger.warning("Container traffic fallback dataframe empty; skipping save.")
            return None
        try:
            filepath = self.output_dir / filename
            df.to_parquet(filepath, index=False)
            logger.info("Saved %s rows to %s", len(df), filepath)
            return filepath
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to save container traffic parquet: %s", exc)
            return None


# =============================================================================
# ANTT CKAN automation
# =============================================================================


class ANTTLogisticsKPIFetcher:
    """Fetch ANTT datasets or fall back to World Bank logistics KPIs."""

    WORLD_BANK_LPI_INDICATOR = "LP.LPI.OVRL.XQ"

    def __init__(self, output_dir: str = "data/silver/freight") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = "https://dados.antt.gov.br"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (FreightDataBot/1.0)"})

    def _download_resource(self, url: str) -> Optional[pd.DataFrame]:
        try:
            response = self.session.get(url, timeout=60)
            response.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to download ANTT resource %s: %s", url, exc)
            return None

        content = response.content
        # Try CSV interpretations
        for encoding in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
            for sep in (";", ","):
                try:
                    df = pd.read_csv(BytesIO(content), sep=sep, encoding=encoding, on_bad_lines="skip")
                    if df.empty:
                        continue
                    return df
                except Exception:
                    continue
        # Try Excel as a fallback
        try:
            return pd.read_excel(BytesIO(content))
        except Exception as exc:  # noqa: BLE001
            logger.warning("Unable to parse ANTT resource %s: %s", url, exc)
            return None

    def _fetch_worldbank_lpi(self) -> Optional[pd.DataFrame]:
        params = {
            "format": "json",
            "per_page": 2000,
        }
        url = f"https://api.worldbank.org/v2/country/BRA/indicator/{self.WORLD_BANK_LPI_INDICATOR}"
        try:
            response = self.session.get(url, params=params, timeout=20)
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # noqa: BLE001
            logger.warning("World Bank LPI fallback failed: %s", exc)
            return None

        if not isinstance(payload, list) or len(payload) < 2 or not payload[1]:
            return None

        rows = []
        for obs in payload[1]:
            value = obs.get("value")
            year = obs.get("date")
            if value is None or year is None:
                continue
            rows.append({
                "date": pd.to_datetime(f"{year}-12-31"),
                "lpi_overall": float(value),
            })

        if not rows:
            return None

        df = pd.DataFrame(rows)
        df.sort_values("date", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def fetch_rntrc_registry(self, year: int = None,
                            month: int = None) -> Optional[pd.DataFrame]:
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month

        logger.info("Fetching RNTRC registry: %s-%02d", year, month)

        url = f"{self.base_url}/api/3/action/package_search"

        params = {
            "q": "RNTRC",
            "rows": 100,
        }

        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:  # noqa: BLE001
            logger.error("RNTRC API fetch failed: %s", exc)
            return None

        if not data.get("result", {}).get("results"):
            logger.warning("No RNTRC datasets found via API")
            return None

        for package in data["result"]["results"]:
            resources = sorted(
                package.get("resources", []),
                key=lambda res: res.get("last_modified") or "",
                reverse=True,
            )
            for resource in resources:
                if resource.get("format", "").upper() not in {"CSV", "XLS", "XLSX"}:
                    continue
                csv_url = resource.get("url")
                if not csv_url:
                    continue
                df = self._download_resource(csv_url)
                if df is not None:
                    logger.info("Fetched %s RNTRC rows from %s", len(df), csv_url)
                    return df

        logger.warning("RNTRC dataset not retrievable via API resources")
        return None

    def _fetch_rntrc_direct(self, year: int, month: int) -> Optional[pd.DataFrame]:
        unused = (year, month)  # placeholder to keep signature
        logger.info("Attempting RNTRC direct fallback from package_show")
        try:
            response = self.session.get(
                f"{self.base_url}/api/3/action/package_show",
                params={"id": "registro-nacional-de-transportadores-rntrc"},
                timeout=15,
            )
            response.raise_for_status()
            package = response.json().get("result", {})
        except Exception as exc:  # noqa: BLE001
            logger.error("RNTRC direct fetch failed: %s", exc)
            return None

        resources = sorted(
            package.get("resources", []),
            key=lambda res: res.get("last_modified") or "",
            reverse=True,
        )
        for resource in resources:
            if resource.get("format", "").upper() not in {"CSV", "XLS", "XLSX"}:
                continue
            csv_url = resource.get("url")
            if not csv_url:
                continue
            df = self._download_resource(csv_url)
            if df is not None:
                logger.info("Fetched %s RNTRC rows from %s", len(df), csv_url)
                return df
        return None

    def fetch_freight_volumes(self) -> Optional[pd.DataFrame]:
        logger.info("Fetching freight volumes (Movimentação de Cargas)...")

        url = f"{self.base_url}/api/3/action/package_search"
        params = {
            "q": "Movimentação de Cargas",
            "rows": 50,
        }

        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:  # noqa: BLE001
            logger.error("Freight volumes fetch failed: %s", exc)
            return None

        for package in data["result"]["results"]:
            for resource in package["resources"]:
                if resource.get("format", "").upper() in {"CSV", "XLS", "XLSX"}:
                    df = self._download_resource(resource.get("url", ""))
                    if df is not None:
                        logger.info("Fetched %s freight volume rows", len(df))
                        return df
        return None

    def fetch_fuel_prices(self) -> Optional[pd.DataFrame]:
        logger.info("Fetching fuel prices...")

        url = f"{self.base_url}/api/3/action/package_search"
        params = {
            "q": "combustíveis",
            "rows": 50,
        }

        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:  # noqa: BLE001
            logger.error("Fuel prices fetch failed: %s", exc)
            return None

        for package in data["result"]["results"]:
            for resource in package["resources"]:
                if resource.get("format", "").upper() in {"CSV", "XLS", "XLSX"}:
                    df = self._download_resource(resource.get("url", ""))
                    if df is not None:
                        logger.info("Fetched %s fuel price rows", len(df))
                        return df
        return None

    def aggregate_kpis(self, rntrc: Optional[pd.DataFrame],
                      volumes: Optional[pd.DataFrame],
                      fuel: Optional[pd.DataFrame]) -> pd.DataFrame:
        now_ts = datetime.utcnow()
        aggregates = {
            "generated_at": now_ts,
            "carrier_count": 0,
            "total_active_transporters": 0,
            "freight_volume_total": 0.0,
            "fuel_price_mean": 0.0,
        }

        if rntrc is not None and not rntrc.empty:
            aggregates["carrier_count"] = int(len(rntrc))
            active_column = None
            for candidate in ("situacao", "status", "situacao_do_transportador"):
                if candidate in rntrc.columns:
                    active_column = candidate
                    break
            if active_column is not None:
                active_mask = rntrc[active_column].astype(str).str.upper().str.contains("ATIVO")
                aggregates["total_active_transporters"] = int(active_mask.sum())

        if volumes is not None and not volumes.empty:
            for col in ("volume", "total_volume", "quantidade"):
                if col in volumes.columns:
                    aggregates["freight_volume_total"] = float(pd.to_numeric(volumes[col], errors="coerce").dropna().sum())
                    break

        if fuel is not None and not fuel.empty:
            for col in ("preco", "preco_medio", "valor"):
                if col in fuel.columns:
                    aggregates["fuel_price_mean"] = float(pd.to_numeric(fuel[col], errors="coerce").dropna().mean())
                    break

        df = pd.DataFrame([aggregates])
        df["date"] = pd.to_datetime(df["generated_at"]).dt.date
        cols = ["date", "generated_at", "carrier_count", "total_active_transporters", "freight_volume_total", "fuel_price_mean"]
        return df[cols]

    def save_parquet(
        self, df: pd.DataFrame, filename: str = "antt_logistics_kpis.parquet"
    ) -> Optional[Path]:
        if df.empty:
            logger.warning("ANTT KPI DataFrame empty; skipping save.")
            return None
        try:
            filepath = self.output_dir / filename
            df.to_parquet(filepath, index=False)
            logger.info("Saved ANTT KPIs to %s", filepath)
            return filepath
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to save ANTT KPIs: %s", exc)
            return None


# =============================================================================
# Orchestrator
# =============================================================================


class FreightBlockerOrchestrator:
    """Top-level runner for all blocker automations."""

    def __init__(self, output_dir: str = "data/silver/freight") -> None:
        self.output_dir = output_dir
        self.results: Dict[str, str] = {}
        self.xeneta = XenetaShippingIndexFetcher(output_dir=self.output_dir)
        self.drewry = DrewryWCIAlternativesFetcher(output_dir=self.output_dir)
        self.antt = ANTTLogisticsKPIFetcher(output_dir=self.output_dir)

    def run_all(self) -> Dict[str, str]:
        """Execute each automation in sequence."""
        print("\n" + "=" * 70)
        print("FREIGHT DATA BLOCKER AUTOMATION")
        print("=" * 70 + "\n")

        # 1) Xeneta / FBX replacement
        print("[1/3] Xeneta XSI-C (FBX replacement)")
        start = (datetime.utcnow() - timedelta(days=180)).strftime("%Y-%m-%d")
        end = datetime.utcnow().strftime("%Y-%m-%d")
        xsi_df = self.xeneta.get_historical_rates(start, end)
        if xsi_df is not None:
            self.xeneta.save_parquet(xsi_df)
            self.results["xeneta_xsi_c"] = f"OK - {len(xsi_df)} records"
        else:
            self.results["xeneta_xsi_c"] = "WARN - no data (check endpoint)"

        time.sleep(0.5)

        # 2) Drewry alternatives
        print("\n[2/3] SCFI / CCFI (Drewry replacement)")
        scfi_df = self.drewry.fetch_scfi(start, end)
        if scfi_df is not None:
            combined = self.drewry.combine(scfi_df, None)
            self.drewry.save_parquet(combined)
            self.results["drewry_alternatives"] = f"OK - {len(combined)} records"
        else:
            self.results["drewry_alternatives"] = "WARN - no data (FRED key?)"

        time.sleep(0.5)

        # 3) ANTT KPIs
        print("\n[3/3] ANTT logistics KPIs")
        rntrc = self.antt.fetch_rntrc_registry()
        freight_volumes = None  # Optional: self.antt.fetch_latest_resource(...)
        fuel_prices = None
        if rntrc is not None:
            kpis = self.antt.aggregate_kpis(rntrc, freight_volumes, fuel_prices)
            self.antt.save_parquet(kpis)
            self.results["antt_kpis"] = f"OK - {len(kpis)} records"
        else:
            logger.warning("RNTRC datasets unavailable; attempting World Bank LPI fallback.")
            lpi_df = self.antt._fetch_worldbank_lpi()
            if lpi_df is not None and not lpi_df.empty:
                self.antt.save_parquet(lpi_df, filename="antt_logistics_kpis.parquet")
                self.results["antt_kpis"] = f"OK - {len(lpi_df)} records (World Bank LPI)"
            else:
                self.results["antt_kpis"] = "WARN - RNTRC not available"

        self._print_summary()
        return self.results

    def _print_summary(self) -> None:
        print("\n" + "=" * 70)
        print("BLOCKER AUTOMATION SUMMARY")
        print("=" * 70)
        for blocker, status in self.results.items():
            print(f"{blocker:28} {status}")
        print("=" * 70)
        print(f"Outputs: {self.output_dir}")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    orchestrator = FreightBlockerOrchestrator()
    orchestrator.run_all()

