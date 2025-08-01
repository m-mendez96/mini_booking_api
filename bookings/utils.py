from datetime import datetime

import requests


def get_nz_public_holidays(year: int) -> list[datetime.date]:
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/NZ"
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        raise Exception("Could not get NZ holidays")

    holidays = response.json()
    return [datetime.strptime(day["date"], "%Y-%m-%d").date() for day in holidays]


def get_current_weather(lat: float, lon: float) -> dict:
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception("Could not get current weather")

    data = response.json()
    weather = data.get("current_weather", {})
    return {
        "temperature": weather.get("temperature"),
        "wind_speed": weather.get("windspeed"),
    }
