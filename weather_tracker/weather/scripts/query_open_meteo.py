import csv
import requests
from collections import defaultdict
from datetime import date
import time
import os

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

BASELINE_START = 2011
BASELINE_END = 2020
YEARS_BACK = 10
END_YEAR = date.today().year - 1

MAX_CITIES = 15
INPUT_CITIES = "top100cities.csv"
OUTPUT_CSV = "weather/seed/demo_weather_data_v3.csv"

SLEEP_SECONDS = 2  # between successful requests


session = requests.Session()
session.headers.update({
    "User-Agent": "weather-tracker-seed-script/1.0"
})


def geocode_city(city):
    r = session.get(
        GEOCODE_URL,
        params={"name": city, "count": 1, "country_code": "US"},
        timeout=20
    )
    r.raise_for_status()
    results = r.json().get("results")
    if not results:
        raise RuntimeError(f"No geocode result for {city}")
    return results[0]["latitude"], results[0]["longitude"], results[0]["name"]


def get_with_backoff(url, params, timeout=30, max_tries=8):
    for attempt in range(1, max_tries + 1):
        try:
            r = session.get(url, params=params, timeout=timeout)

            if r.status_code == 429:
                retry_after = r.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    wait = int(retry_after)
                else:
                    wait = 30 * attempt
                print(f"429 Too Many Requests. Sleeping {wait}s (attempt {attempt}/{max_tries})...")
                time.sleep(wait)
                continue

            r.raise_for_status()
            return r

        except requests.exceptions.RequestException as e:
            wait = 10 * attempt
            print(f"Request error: {e}. Sleeping {wait}s (attempt {attempt}/{max_tries})...")
            time.sleep(wait)

    raise RuntimeError("Failed after repeated retries/backoff.")


def fetch_daily(lat, lon, start_date, end_date):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": "fahrenheit",
        "timezone": "auto",
    }
    r = get_with_backoff(ARCHIVE_URL, params=params, timeout=30, max_tries=8)
    daily = r.json()["daily"]
    return daily["time"], daily["temperature_2m_max"], daily["temperature_2m_min"]


def fetch_daily_year(lat, lon, year):
    return fetch_daily(lat, lon, f"{year}-01-01", f"{year}-12-31")


# ------------------
# LOAD CITIES
# ------------------

with open(INPUT_CITIES, newline="", encoding="utf-8") as f:
    cities = list(csv.DictReader(f))[:MAX_CITIES]

rows = []

# ------------------
# MAIN LOOP
# ------------------

for i, row in enumerate(cities, start=1):
    city = row["city"]
    state = row["state"]
    print(f"[{i}/{len(cities)}] {city}, {state}")

    lat, lon, resolved_name = geocode_city(city)
    time.sleep(SLEEP_SECONDS)

    # ---- baseline counts by year ----
    base_above_90 = {}
    base_below_32 = {}

    for y in range(BASELINE_START, BASELINE_END + 1):
        dates, tmaxs, tmins = fetch_daily_year(lat, lon, y)
        time.sleep(SLEEP_SECONDS)

        hot = 0
        cold = 0
        for tmax, tmin in zip(tmaxs, tmins):
            if tmax > 90:
                hot += 1
            if tmin < 32:
                cold += 1

        base_above_90[y] = hot
        base_below_32[y] = cold

    baseline_years = (BASELINE_END - BASELINE_START + 1)
    baseline_avg_above_90 = sum(base_above_90.values()) / baseline_years
    baseline_avg_below_32 = sum(base_below_32.values()) / baseline_years

    # ---- recent years (last 10 complete years) ----
    start_year = END_YEAR - YEARS_BACK + 1

    for y in range(start_year, END_YEAR + 1):
        dates, tmaxs, tmins = fetch_daily_year(lat, lon, y)
        time.sleep(SLEEP_SECONDS)

        hot = 0
        cold = 0
        for tmax, tmin in zip(tmaxs, tmins):
            if tmax > 90:
                hot += 1
            if tmin < 32:
                cold += 1

        rows.append({
            "location_name": resolved_name,
            "state": state,
            "latitude": lat,
            "longitude": lon,
            "metric": "days_above_90f",
            "target_year": y,
            "baseline_start_year": BASELINE_START,
            "baseline_end_year": BASELINE_END,
            "target_value": hot,
            "baseline_avg_value": baseline_avg_above_90,
            "delta_value": hot - baseline_avg_above_90,
            "status": "completed",
        })

        rows.append({
            "location_name": resolved_name,
            "state": state,
            "latitude": lat,
            "longitude": lon,
            "metric": "days_below_32f",
            "target_year": y,
            "baseline_start_year": BASELINE_START,
            "baseline_end_year": BASELINE_END,
            "target_value": cold,
            "baseline_avg_value": baseline_avg_below_32,
            "delta_value": cold - baseline_avg_below_32,
            "status": "completed",
        })


# ------------------
# WRITE CSV
# ------------------

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "location_name",
            "state",
            "latitude",
            "longitude",
            "metric",
            "target_year",
            "baseline_start_year",
            "baseline_end_year",
            "target_value",
            "baseline_avg_value",
            "delta_value",
            "status",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"\nWrote {len(rows)} rows to {OUTPUT_CSV}")
