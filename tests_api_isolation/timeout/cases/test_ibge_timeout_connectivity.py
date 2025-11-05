import pytest
import requests


@pytest.mark.parametrize("state_code", ["29", "35"], ids=["bahia", "sao_paulo"])
def test_ibge_timeout_connectivity(run_live, timeout, state_code, trace_writer):
    if not run_live:
        pytest.skip("Set RUN_LIVE=1 to execute live IBGE tests")

    url = f"https://servicodados.ibge.gov.br/api/v1/economia/pib/v2/{state_code}/2024"
    kwargs = {}
    if timeout is not None:
        kwargs["timeout"] = timeout

    response = requests.get(url, **kwargs)
    trace_writer(
        endpoint_name="ibge_connectivity",
        variation={
            "state_code": state_code,
            "timeout": timeout,
        },
        metrics={
            "status": response.status_code,
            "body_sample": response.json()[:1] if response.headers.get("Content-Type", "").startswith("application/json") else response.text,
        },
    )

    assert response.status_code == 200, f"Unexpected status {response.status_code} for {url}"
    payload = response.json()
    assert isinstance(payload, list)
    if payload:
        assert "municipio" in payload[0] or "variavel" in payload[0]
