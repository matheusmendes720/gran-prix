import os

import pytest
import requests


@pytest.mark.parametrize("use_key", [True, False], ids=["with_key", "without_key"])
@pytest.mark.parametrize("units", ["metric", "imperial"], ids=["metric", "imperial"])
def test_openweather_auth_and_timeout(run_live, openweather_base, timeout, use_key, units, trace_writer):
    if not run_live:
        pytest.skip("Set RUN_LIVE=1 to execute live OpenWeather tests")

    api_key = os.getenv("OPENWEATHER_API_KEY") if use_key else ""
    city = os.getenv("OPENWEATHER_CITY", "Salvador,BR")

    if use_key and not api_key:
        pytest.skip("OPENWEATHER_API_KEY not configured for authenticated test")

    params = {"q": city, "appid": api_key, "units": units}

    kwargs = {"params": params}
    if timeout is not None:
        kwargs["timeout"] = timeout

    try:
        response = requests.get(openweather_base, **kwargs)
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"OpenWeather request failed: {exc}")

    trace_writer(
        endpoint_name="openweather_auth",
        variation={
            "use_key": use_key,
            "units": units,
            "timeout": timeout,
        },
        metrics={
            "status": response.status_code,
            "headers": dict(response.headers),
        },
    )

    if use_key and api_key:
        assert response.status_code == 200, f"Expected 200 with API key, received {response.status_code}"
        payload = response.json()
        assert "weather" in payload and "main" in payload
    else:
        assert response.status_code in {401, 403}, "Unauthenticated request should fail"
