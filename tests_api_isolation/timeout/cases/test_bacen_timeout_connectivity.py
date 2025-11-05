import json
import time
from typing import Optional

import pytest
import requests


@pytest.mark.parametrize("series_name", ["exchange_rate", "ipca"], ids=["exchange_rate", "ipca"])
def test_bacen_connectivity(run_live, bacen_base, bacen_series_codes, timeout, max_retries, trace_writer, series_name):
    if not run_live:
        pytest.skip("Set RUN_LIVE=1 to execute live BACEN connectivity tests")

    series = bacen_series_codes[series_name]
    url = f"{bacen_base}{series}/dados"
    params = {
        "formato": "json",
        "dataInicial": "01/01/2024",
        "dataFinal": "31/12/2024",
    }

    attempt = 0
    response_times = []
    status = None
    last_error: Optional[str] = None

    while attempt <= max_retries:
        attempt += 1
        try:
            start = time.perf_counter()
            kwargs = {"params": params}
            if timeout is not None:
                kwargs["timeout"] = timeout
            response = requests.get(url, **kwargs)
            elapsed = time.perf_counter() - start
            response_times.append(elapsed)
            status = response.status_code

            if 200 <= response.status_code < 300:
                body = response.json()
                assert isinstance(body, list)
                if body:
                    assert "data" in body[0] and "valor" in body[0]
                trace_writer(
                    endpoint_name="bacen_connectivity",
                    variation={
                        "series": series_name,
                        "timeout": timeout,
                        "max_retries": max_retries,
                    },
                    metrics={
                        "status": response.status_code,
                        "attempts": attempt,
                        "response_times": response_times,
                        "body_sample": body[:2],
                    },
                )
                return

            if response.status_code in {400, 401, 403, 404}:
                pytest.skip(f"Client error {response.status_code} for {url}")

            last_error = f"HTTP {response.status_code}"

        except requests.exceptions.Timeout:
            last_error = "timeout"
        except requests.exceptions.RequestException as exc:
            last_error = str(exc)

        if attempt <= max_retries:
            time.sleep(0.5 * attempt)

    trace_writer(
        endpoint_name="bacen_connectivity",
        variation={
            "series": series_name,
            "timeout": timeout,
            "max_retries": max_retries,
        },
        metrics={
            "status": status,
            "attempts": attempt,
            "error": last_error,
            "response_times": response_times,
        },
    )
    pytest.fail(f"Failed after {attempt} attempts: {last_error}")
