import pytest
import requests


@pytest.mark.parametrize(
    "url",
    [
        "https://www.gov.br/anatel/",
        "https://dadosabertos.anatel.gov.br/",
    ],
    ids=["portal", "dados_abertos"],
)
def test_anatel_timeout_connectivity(run_live, timeout, url, trace_writer):
    if not run_live:
        pytest.skip("Set RUN_LIVE=1 to execute live ANATEL tests")

    kwargs = {}
    if timeout is not None:
        kwargs["timeout"] = timeout

    response = requests.get(url, **kwargs)
    trace_writer(
        endpoint_name="anatel_connectivity",
        variation={
            "url": url,
            "timeout": timeout,
        },
        metrics={
            "status": response.status_code,
            "headers": dict(response.headers),
        },
    )

    assert response.status_code in {200, 301, 302}, f"Unexpected status {response.status_code} for {url}"
