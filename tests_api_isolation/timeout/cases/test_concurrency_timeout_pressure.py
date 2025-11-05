from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean
from typing import List

import pytest
import requests


@pytest.mark.parametrize("parallelism", [1, 5, 20], ids=["p1", "p5", "p20"])
def test_bacen_concurrency_pressure(run_live, bacen_base, bacen_series_codes, timeout, parallelism, trace_writer):
    if not run_live:
        pytest.skip("Set RUN_LIVE=1 to execute concurrency pressure tests")

    url = f"{bacen_base}{bacen_series_codes['ipca']}/dados"
    params = {
        "formato": "json",
        "dataInicial": "01/01/2024",
        "dataFinal": "31/12/2024",
    }

    def do_call():
        kwargs = {"params": params}
        if timeout is not None:
            kwargs["timeout"] = timeout
        response = requests.get(url, **kwargs)
        return response.status_code

    statuses: List[int] = []
    with ThreadPoolExecutor(max_workers=parallelism) as executor:
        futures = [executor.submit(do_call) for _ in range(parallelism)]
        for future in as_completed(futures):
            statuses.append(future.result())

    success = sum(1 for status in statuses if 200 <= status < 300)
    success_ratio = success / len(statuses)
    trace_writer(
        endpoint_name="bacen_concurrency",
        variation={
            "parallelism": parallelism,
            "timeout": timeout,
        },
        metrics={
            "statuses": statuses,
            "success_ratio": success_ratio,
        },
    )

    assert success_ratio >= 0.8, f"Success ratio too low: {success_ratio:.2%}"
