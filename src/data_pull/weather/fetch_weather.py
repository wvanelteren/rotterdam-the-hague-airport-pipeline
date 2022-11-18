import json
import os
from typing import Any

import requests
from dotenv import load_dotenv
from dataclasses import dataclass

from src.data_pull.weather.aiport_loc import AirportLoc

load_dotenv()

API_KEY: str = os.environ.get("OPENWEATHER_API_KEY")
API_URL: str = "http://api.openweathermap.org/data/2.5/weather?"


def fetch_weather_info() -> dict[str, Any]:
    target_url: str = (
        API_URL +
        "lat=" + AirportLoc().LAT +
        "&lon=" + AirportLoc().LON +
        "&units=metric" +
        "&appid=" + API_KEY
    )
    try:
        response: dict[str, Any] = requests.get(target_url).json()
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except json.JSONDecodeError as err:
        raise SystemExit(err)

        
@dataclass
class Weather():
    condition: str
    temp: float
    pressure: int
    humidity: int
    visibility: int
    wind_speed: float
    wind_direction: int
    cloudiness: int


@dataclass
class NightTime():
    sunrise: int
    sunset: int

