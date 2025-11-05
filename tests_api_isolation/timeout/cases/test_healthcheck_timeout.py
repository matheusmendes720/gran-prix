import pytest
import requests


@pytest.mark.parametrize("expected_status", [200, 503], ids=["healthy", "degraded"])
def test_healthcheck_timeout_behavior(run_live, healthcheck_url, timeout, expected_status, trace_writer):
    if not run_live:
        pytest.skip("Set RUN_LIVE=1 to execute health check tests")

    kwargs = {}
    if timeout is not None:
        kwargs["timeout"] = timeout

    response = requests.get(healthcheck_url, **kwargs)
    trace_writer(
        endpoint_name="healthcheck",
        variation={
            "timeout": timeout,
            "expected_status": expected_status,
        },
        metrics={
            "status": response.status_code,
            "body": response.json() if response.headers.get("Content-Type", "").startswith("application/json") else response.text,
        },
    )

    if expected_status == 200:
        assert response.status_code == 200
        payload = response.json()
        assert payload.get("status") in {"healthy", "degraded"}
    else:
        assert response.status_code in {200, 503}
