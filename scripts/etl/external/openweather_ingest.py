"""
OpenWeather ingestion utilities.

Downloads geocoding data, historical weather (One Call API), 5-day forecasts
and optional 16-day daily forecasts for a list of Brazilian cities defined in
``config/openweather_cities.json``. Results are written to the landing zone
``data/landing/external_factors-raw/openweather`` using the structure:

    city_slug/YYYYMMDD/{onecall_history.json, forecast_5day.json, forecast_daily.json}

Geocoding results are cached in ``data/reference/openweather_geocoding.csv`` so
subsequent runs do not hit the Geocoding API unnecessarily.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import requests

from . import configure_logging, ensure_directory


BASE_DIR = Path("data/landing/external_factors-raw/openweather")
REFERENCE_DIR = Path("data/reference")
GEOCODING_CACHE = REFERENCE_DIR / "openweather_geocoding.csv"
CONFIG_PATH = Path("config/openweather_cities.json")

GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
ONECALL_HISTORY_URL = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
FORECAST_5DAY_URL = "https://api.openweathermap.org/data/2.5/forecast"
FORECAST_DAILY_URL = "https://api.openweathermap.org/data/2.5/forecast/daily"
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENMETEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

REQUEST_TIMEOUT = 60

logger = configure_logging("openweather")


class OpenWeatherError(RuntimeError):
    """Raised when the OpenWeather API returns an unsuccessful response."""


def load_api_key() -> str:
    key = os.environ.get("OPENWEATHER_API_KEY")
    if not key:
        raise OpenWeatherError(
            "OPENWEATHER_API_KEY environment variable not set. "
            "Please export it before running the ingestion script."
        )
    return key


def load_config(path: Path = CONFIG_PATH) -> List[Dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file {path} not found. "
            "Create config/openweather_cities.json first."
        )
    with path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    cities = data.get("cities", [])
    if not cities:
        raise ValueError("No cities found inside openweather configuration.")
    return cities


def load_geocoding_cache() -> Dict[str, Dict]:
    if not GEOCODING_CACHE.exists():
        ensure_directory(REFERENCE_DIR)
        return {}

    cache: Dict[str, Dict] = {}
    with GEOCODING_CACHE.open("r", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            cache[row["slug"]] = {
                "name": row["name"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "country": row.get("country"),
                "state": row.get("state"),
                "city_id": int(row["city_id"]) if row.get("city_id") else None,
                "last_updated": row.get("last_updated"),
            }
    return cache


def write_geocoding_cache(cache: Dict[str, Dict]) -> None:
    ensure_directory(REFERENCE_DIR)
    with GEOCODING_CACHE.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["slug", "name", "lat", "lon", "country", "state", "city_id", "last_updated"])
        for slug, info in sorted(cache.items()):
            writer.writerow(
                [
                    slug,
                    info.get("name"),
                    info.get("lat"),
                    info.get("lon"),
                    info.get("country"),
                    info.get("state"),
                    info.get("city_id"),
                    info.get("last_updated"),
                ]
            )


def geocode_city(city: Dict, api_key: str, cache: Dict[str, Dict]) -> Dict:
    slug = city["slug"]
    if slug in cache:
        return cache[slug]

    params = {
        "q": ",".join(filter(None, [city["name"], city.get("state"), city.get("country")])),
        "limit": 1,
        "appid": api_key,
    }
    logger.info("Geocoding %s", params["q"])
    resp = requests.get(GEOCODE_URL, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        raise OpenWeatherError(f"Geocoding returned no results for {params['q']}")

    data = results[0]
    cache_entry = {
        "name": data["name"],
        "lat": data["lat"],
        "lon": data["lon"],
        "country": data.get("country"),
        "state": data.get("state"),
        "city_id": city.get("city_id"),
        "last_updated": datetime.utcnow().isoformat(),
    }
    cache[slug] = cache_entry
    write_geocoding_cache(cache)
    return cache_entry


def fallback_coordinates_from_city_id(city_id: int, api_key: str) -> Optional[Dict]:
    params = {"id": city_id, "appid": api_key}
    resp = requests.get(CURRENT_WEATHER_URL, params=params, timeout=REQUEST_TIMEOUT)
    if resp.status_code != 200:
        return None
    data = resp.json()
    coord = data.get("coord")
    if not coord:
        return None
    return {
        "lat": coord["lat"],
        "lon": coord["lon"],
        "name": data.get("name"),
        "country": data.get("sys", {}).get("country"),
    }


def ensure_coordinates(city: Dict, api_key: str, cache: Dict[str, Dict]) -> Dict:
    slug = city["slug"]
    cache_entry = cache.get(slug)

    if cache_entry and cache_entry.get("lat") is not None and cache_entry.get("lon") is not None:
        return cache_entry

    if city.get("lat") is not None and city.get("lon") is not None:
        cache_entry = {
            "name": city.get("name"),
            "lat": city["lat"],
            "lon": city["lon"],
            "country": city.get("country"),
            "state": city.get("state"),
            "city_id": city.get("city_id"),
            "last_updated": datetime.utcnow().isoformat(),
        }
        cache[slug] = cache_entry
        write_geocoding_cache(cache)
        return cache_entry

    if cache_entry and cache_entry.get("lat") is not None and cache_entry.get("lon") is not None:
        return cache_entry

    if city.get("city_id"):
        fallback = fallback_coordinates_from_city_id(city["city_id"], api_key)
        if fallback:
            cache_entry = {
                "name": fallback.get("name") or city["name"],
                "lat": fallback["lat"],
                "lon": fallback["lon"],
                "country": fallback.get("country") or city.get("country"),
                "state": city.get("state"),
                "city_id": city["city_id"],
                "last_updated": datetime.utcnow().isoformat(),
            }
            cache[slug] = cache_entry
            write_geocoding_cache(cache)
            return cache_entry

    return geocode_city(city, api_key, cache)


def fetch_onecall_history(lat: float, lon: float, api_key: str, days: int = 5) -> List[Dict]:
    days = min(days, 5)  # API limit
    results: List[Dict] = []
    for offset in range(1, days + 1):
        target_dt = datetime.utcnow() - timedelta(days=offset)
        params = {
            "lat": lat,
            "lon": lon,
            "dt": int(target_dt.timestamp()),
            "units": "metric",
            "appid": api_key,
        }
        logger.info(
            "Fetching hourly history for lat=%s lon=%s date=%s",
            lat,
            lon,
            target_dt.date(),
        )
        try:
            resp = requests.get(ONECALL_HISTORY_URL, params=params, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
        except requests.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else None
            if status_code in (401, 403):
                logger.warning(
                    "One Call history not available for lat=%s lon=%s (status %s). Falling back to Open-Meteo.",
                    lat,
                    lon,
                    status_code,
                )
                return []
            raise
        results.append(resp.json())
        time.sleep(1)  # respect rate limit
    return results


def fetch_openmeteo_history(lat: float, lon: float, days: int = 5) -> Optional[Dict]:
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "UTC",
    }
    logger.info(
        "Fetching Open-Meteo archive for lat=%s lon=%s (%s -> %s)",
        lat,
        lon,
        params["start_date"],
        params["end_date"],
    )
    resp = requests.get(OPENMETEO_ARCHIVE_URL, params=params, timeout=REQUEST_TIMEOUT)
    if resp.status_code != 200:
        logger.warning(
            "Open-Meteo fallback failed for lat=%s lon=%s (status %s)",
            lat,
            lon,
            resp.status_code,
        )
        return None
    return resp.json()


def fetch_forecast(lat: float, lon: float, api_key: str) -> Dict:
    params = {"lat": lat, "lon": lon, "units": "metric", "appid": api_key}
    logger.info("Fetching 5-day forecast for lat=%s lon=%s", lat, lon)
    resp = requests.get(FORECAST_5DAY_URL, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fetch_daily_forecast(lat: float, lon: float, api_key: str, cnt: int = 16) -> Dict:
    params = {
        "lat": lat,
        "lon": lon,
        "cnt": cnt,
        "units": "metric",
        "appid": api_key,
        "lang": "pt_br",
    }
    logger.info("Fetching daily forecast (cnt=%s) for lat=%s lon=%s", cnt, lat, lon)
    resp = requests.get(FORECAST_DAILY_URL, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def write_json(data: Dict | List, output_path: Path) -> None:
    ensure_directory(output_path.parent)
    with output_path.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def process_city(city: Dict, api_key: str, options: argparse.Namespace, cache: Dict[str, Dict]) -> None:
    slug = city["slug"]
    cache_entry = ensure_coordinates(city, api_key, cache)
    lat, lon = cache_entry["lat"], cache_entry["lon"]

    today_str = datetime.utcnow().strftime("%Y%m%d")
    base_path = BASE_DIR / slug / today_str

    if not options.skip_history:
        history = fetch_onecall_history(lat, lon, api_key, city.get("history_days", options.history_days))
        if history:
            write_json(history, base_path / "onecall_history.json")
        else:
            fallback_history = fetch_openmeteo_history(lat, lon, city.get("history_days", options.history_days))
            if fallback_history:
                write_json(fallback_history, base_path / "openmeteo_history.json")

    if not options.skip_forecast:
        try:
            forecast = fetch_forecast(lat, lon, api_key)
            write_json(forecast, base_path / "forecast_5day.json")
        except requests.HTTPError as exc:
            logger.warning("5-day forecast failed for %s: %s", slug, exc)

    if options.daily_forecast or city.get("enable_daily_forecast"):
        try:
            daily = fetch_daily_forecast(lat, lon, api_key, cnt=options.daily_days)
            write_json(daily, base_path / "forecast_daily.json")
        except requests.HTTPError as exc:
            logger.warning("Daily forecast failed for %s: %s", slug, exc)


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download OpenWeather historical and forecast data.")
    parser.add_argument(
        "--config",
        type=Path,
        default=CONFIG_PATH,
        help="Path to JSON configuration file (default: config/openweather_cities.json)",
    )
    parser.add_argument(
        "--history-days",
        type=int,
        default=5,
        help="Number of past days to download with OneCall (max 5)",
    )
    parser.add_argument(
        "--skip-history",
        action="store_true",
        help="Skip downloading One Call historical data",
    )
    parser.add_argument(
        "--skip-forecast",
        action="store_true",
        help="Skip downloading 5-day forecast data",
    )
    parser.add_argument(
        "--daily-forecast",
        action="store_true",
        help="Force download of 16-day daily forecast regardless of config flag",
    )
    parser.add_argument(
        "--daily-days",
        type=int,
        default=16,
        help="Number of days to fetch in the daily forecast (max 16)",
    )
    return parser.parse_args(args)


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    api_key = load_api_key()
    cities = load_config(options.config)
    cache = load_geocoding_cache()

    for city in cities:
        try:
            process_city(city, api_key, options, cache)
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Failed to process city %s: %s", city.get("slug") or city.get("name"), exc)
            continue

    logger.info("OpenWeather ingestion completed.")


if __name__ == "__main__":
    main()

