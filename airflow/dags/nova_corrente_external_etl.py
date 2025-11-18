"""
Airflow DAG orchestrating external data ingestion for Nova Corrente.

The DAG triggers the Python modules responsible for downloading OpenWeather,
BACEN, IBGE and World Bank datasets. Tasks run sequentially to ensure macro
series are available before downstream processing.
"""

from __future__ import annotations

import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _make_env() -> dict:
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    return env


def run_module(module: str, args: list[str] | None = None) -> None:
    """
    Execute a Python module located inside the repository using subprocess.

    Parameters
    ----------
    module:
        Dotted module path to pass into ``python -m``.
    args:
        Optional list of CLI arguments to append to the command.
    """

    command = ["python", "-m", module]
    if args:
        command.extend(args)

    subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=True,
        env=_make_env(),
    )


def run_openweather_ingest(**_) -> None:
    run_module("scripts.etl.external.openweather_ingest", ["--daily-forecast"])


def run_bacen_downloader(**_) -> None:
    run_module(
        "scripts.etl.external.bacen_downloader",
        ["--start", "2015-01-01"],
    )


def run_ibge_downloader(**_) -> None:
    run_module("scripts.etl.external.ibge_downloader")


def run_worldbank_downloader(**_) -> None:
    run_module("scripts.etl.external.worldbank_downloader")


def run_freight_blockers(**_) -> None:
    run_module("scripts.automation.freight_blockers.integration", ["run-all"])


default_args = {
    "owner": "nova_corrente",
    "depends_on_past": False,
    "start_date": datetime(2025, 11, 10),
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="nova_corrente_external_etl",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["external", "etl"],
) as dag:
    openweather_task = PythonOperator(
        task_id="openweather_ingest",
        python_callable=run_openweather_ingest,
    )

    bacen_task = PythonOperator(
        task_id="bacen_downloader",
        python_callable=run_bacen_downloader,
    )

    ibge_task = PythonOperator(
        task_id="ibge_downloader",
        python_callable=run_ibge_downloader,
    )

    worldbank_task = PythonOperator(
        task_id="worldbank_downloader",
        python_callable=run_worldbank_downloader,
    )

    freight_blockers_task = PythonOperator(
        task_id="freight_blockers_automation",
        python_callable=run_freight_blockers,
    )

    openweather_task >> bacen_task >> ibge_task >> worldbank_task >> freight_blockers_task

