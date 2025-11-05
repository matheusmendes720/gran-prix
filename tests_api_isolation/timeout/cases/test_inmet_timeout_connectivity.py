import pytest
import requests


@pytest.mark.parametrize(
    "endpoint",
    [
        ("base", "https://apitempo.inmet.gov.br/"),
        ("portal", "https://tempo.inmet.gov.br/"),
    ],
    ids=["base_api", "web_portal"],
)
def test_inmet_timeout_connectivity(run_live, timeout, endpoint, trace_writer):
    if not run_live:
        pytest.skip("Set RUN_LIVE=1 to execute live INMET tests")

    name, url = endpoint
    kwargs = {}
    if timeout is not None:
        kwargs["timeout"] = timeout

    response = requests.get(url, **kwargs)
    trace_writer(
        endpoint_name="inmet_connectivity",
        variation={
            "endpoint": name,
            "timeout": timeout,
        },
        metrics={
            "status": response.status_code,
            "headers": dict(response.headers),
        },
    )

    assert response.status_code in {200, 301, 302}, f"Unexpected status {response.status_code} for {url}"
