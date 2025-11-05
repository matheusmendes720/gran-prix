import time
from typing import Optional

import pytest
import requests


@pytest.mark.parametrize("series_name", ["ipca"], ids=["ipca"])
@pytest.mark.parametrize("retry_backoff", [0.2, 0.5], ids=["backoff_0_2", "backoff_0_5"])
def test_bacen_schema_and_retries(run_live, bacen_base, bacen_series_codes, timeout, max_retries, retry_backoff, trace_writer, series_name):
    if not run_live:
        pytest.skip("Set RUN_LIVE=1 to execute live BACEN schema tests")

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
                payload = response.json()
                assert isinstance(payload, list)
                for record in payload[:5]:
                    assert "data" in record and isinstance(record["data"], str)
                    assert "valor" in record and isinstance(record["valor"], str)
                trace_writer(
                    endpoint_name="bacen_schema",
                    variation={
                        "series": series_name,
                        "timeout": timeout,
                        "max_retries": max_retries,
                        "retry_backoff": retry_backoff,
                    },
                    metrics={
                        "status": response.status_code,
                        "attempts": attempt,
                        "response_times": response_times,
                        "record_count": len(payload),
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
            jitter = retry_backoff * (1 + 0.2)
            time.sleep(retry_backoff + jitter * attempt)

    trace_writer(
        endpoint_name="bacen_schema",
        variation={
            "series": series_name,
            "timeout": timeout,
            "max_retries": max_retries,
            "retry_backoff": retry_backoff,
        },
        metrics={
            "status": status,
            "attempts": attempt,
            "error": last_error,
            "response_times": response_times,
        },
    )
    pytest.fail(f"Schema validation failed after {attempt} attempts: {last_error}")
