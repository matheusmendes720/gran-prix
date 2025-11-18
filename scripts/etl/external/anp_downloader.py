"""
Download ANP semiannual fuel price datasets and aggregate to daily averages.

Data source: https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/
serie-historica-de-precos-de-combustiveis
"""

from __future__ import annotations

import io
import re
import time
import unicodedata
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup

from . import configure_logging, ensure_directory


logger = configure_logging("anp")

PAGE_URL = (
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/"
    "serie-historica-de-precos-de-combustiveis"
)
LANDING_DIR = Path("data/landing/external_factors-raw/logistics/anp_fuel")
START_DATE = pd.Timestamp("2021-01-01")

PRODUCT_MAP = {
    "GASOLINA": "gasoline_common_price",
    "GASOLINA ADITIVADA": "gasoline_premium_price",
    "ETANOL": "ethanol_price",
    "DIESEL": "diesel_price",
    "DIESEL S10": "diesel_s10_price",
    "DIESEL S500": "diesel_s500_price",
    "GNV": "gnv_price",
    "GLP": "glp_price",
}


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch)).upper().strip()


@dataclass
class DataFile:
    url: str
    year: int
    period: str  # e.g., "2024-02"
    is_zip: bool


def fetch_data_file_links() -> List[DataFile]:
    logger.info("Fetching ANP open data page...")
    resp = requests.get(PAGE_URL, timeout=60)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    pattern = re.compile(r"ca-(\d{4})-(\d{2})\.(zip|csv)$", re.IGNORECASE)
    links: List[DataFile] = []

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        match = pattern.search(href)
        if not match:
            continue
        year = int(match.group(1))
        period = f"{match.group(1)}-{match.group(2)}"
        if year < START_DATE.year:
            continue
        is_zip = href.lower().endswith(".zip")
        links.append(DataFile(url=href, year=year, period=period, is_zip=is_zip))

    if not links:
        logger.warning("No ANP data links found on %s", PAGE_URL)
    else:
        logger.info("Found %s ANP data files", len(links))
    return links


def download_bytes(url: str, retries: int = 3, chunk_size: int = 1 << 20) -> bytes:
    last_exc: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
            with requests.get(url, timeout=120, stream=True) as resp:
                resp.raise_for_status()
                chunks = []
                for chunk in resp.iter_content(chunk_size):
                    if chunk:
                        chunks.append(chunk)
                return b"".join(chunks)
        except requests.exceptions.RequestException as exc:
            last_exc = exc
            logger.warning(
                "Attempt %s/%s failed downloading %s: %s",
                attempt,
                retries,
                url,
                exc,
            )
            time.sleep(2 * attempt)
    if last_exc:
        raise last_exc
    raise RuntimeError(f"Failed to download {url}")


def read_csv_from_zip(content: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        members = [name for name in zf.namelist() if name.lower().endswith(".csv")]
        if not members:
            raise ValueError("Zip file does not contain any CSV files.")
        with zf.open(members[0]) as csv_file:
            return pd.read_csv(
                csv_file,
                sep=";",
                decimal=",",
                encoding="latin-1",
                dtype=str,
            )


def read_csv_from_bytes(content: bytes) -> pd.DataFrame:
    return pd.read_csv(
        io.BytesIO(content),
        sep=";",
        decimal=",",
        encoding="latin-1",
        dtype=str,
    )


def download_dataset(data_file: DataFile) -> pd.DataFrame:
    logger.info("Downloading %s", data_file.url)
    content = download_bytes(data_file.url)

    if data_file.is_zip:
        df = read_csv_from_zip(content)
    else:
        df = read_csv_from_bytes(content)

    df.columns = [col.replace("\ufeff", "").strip() for col in df.columns]

    # Normalize column names we need
    required_columns = {
        "Regiao - Sigla",
        "Estado - Sigla",
        "Municipio",
        "Produto",
        "Data da Coleta",
        "Valor de Venda",
    }

    missing = required_columns.difference(df.columns)
    if missing:
        logger.warning(
            "File %s missing expected columns: %s",
            data_file.url,
            ", ".join(sorted(missing)),
        )

    df["Produto"] = df["Produto"].astype(str).apply(normalize_text)
    df["Data da Coleta"] = pd.to_datetime(
        df["Data da Coleta"], dayfirst=True, errors="coerce"
    )
    df = df[df["Data da Coleta"] >= START_DATE]
    df["Valor de Venda"] = pd.to_numeric(df["Valor de Venda"].str.replace(",", "."), errors="coerce")

    df["Produto"] = df["Produto"].map(PRODUCT_MAP)

    df = df.dropna(subset=["Data da Coleta", "Produto", "Valor de Venda"])

    df = df[["Data da Coleta", "Produto", "Valor de Venda"]]
    df["period"] = data_file.period
    return df


def aggregate_prices(data_frames: Iterable[pd.DataFrame]) -> pd.DataFrame:
    combined = pd.concat(data_frames, ignore_index=True)
    grouped = (
        combined.groupby(["Data da Coleta", "Produto"])["Valor de Venda"]
        .mean()
        .reset_index()
        .rename(columns={"Data da Coleta": "date", "Valor de Venda": "price"})
    )
    pivoted = grouped.pivot(index="date", columns="Produto", values="price").reset_index()
    pivoted.sort_values("date", inplace=True)
    return pivoted


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    links = fetch_data_file_links()
    if not links:
        return

    datasets: List[pd.DataFrame] = []
    for data_file in links:
        try:
            df = download_dataset(data_file)
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Failed to download %s: %s", data_file.url, exc)
            continue
        if df.empty:
            logger.warning("Dataset %s is empty after filtering.", data_file.url)
            continue
        datasets.append(df)

    if not datasets:
        logger.warning("No ANP datasets were downloaded successfully.")
        return

    aggregated = aggregate_prices(datasets)
    if aggregated.empty:
        logger.warning("Aggregated ANP dataframe is empty.")
        return

    run_stamp = datetime.utcnow().strftime("%Y%m%d")
    output_dir = LANDING_DIR / run_stamp
    ensure_directory(output_dir)
    output_path = output_dir / "anp_fuel.csv"
    aggregated.to_csv(output_path, index=False)
    logger.info("Saved ANP aggregated dataset with %s rows to %s", len(aggregated), output_path)


if __name__ == "__main__":
    main()

