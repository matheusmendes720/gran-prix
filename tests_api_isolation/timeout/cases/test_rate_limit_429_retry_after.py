import time
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest
import requests


@pytest.mark.parametrize("retry_after", ["1", "2", None], ids=["retry_after_1", "retry_after_2", "no_retry_after"])
@pytest.mark.parametrize("max_retries", [1, 3], ids=["retries_1", "retries_3"])
def test_rate_limit_retry_after_handling(timeout, max_retries, retry_after, trace_writer):
    sequence = []

    def fake_get(url, params=None, timeout=None):  # pragma: no cover - mock behavior
        if not sequence:
            resp = MagicMock()
            resp.status_code = 429
            resp.headers = {"Retry-After": retry_after} if retry_after else {}
            sequence.append("429")
            return resp
        resp = MagicMock()
        resp.status_code = 200
        resp.headers = {}
        resp.json.return_value = [{"data": "02/01/2024", "valor": "4.95"}]
        return resp

    with patch.object(requests, "get", side_effect=fake_get):
        attempts = 0
        status_codes = []
        while attempts <= max_retries:
            attempts += 1
            resp = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados", timeout=timeout or 30)
            status_codes.append(resp.status_code)
            if resp.status_code == 200:
                trace_writer(
                    endpoint_name="bacen_rate_limit",
                    variation={
                        "timeout": timeout,
                        "max_retries": max_retries,
                        "retry_after": retry_after,
                    },
                    metrics={
                        "status_codes": status_codes,
                        "attempts": attempts,
                    },
                )
                return

            assert resp.status_code == 429, f"Unexpected status {resp.status_code}"
            delay = int(resp.headers.get("Retry-After", "1"))
            time.sleep(delay)

        trace_writer(
            endpoint_name="bacen_rate_limit",
            variation={
                "timeout": timeout,
                "max_retries": max_retries,
                "retry_after": retry_after,
            },
            metrics={
                "status_codes": status_codes,
                "attempts": attempts,
                "error": "Exceeded retries",
            },
        )
        pytest.fail("Exceeded max retries without success")
