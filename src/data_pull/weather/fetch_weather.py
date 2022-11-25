import json
import os
from dataclasses import asdict, dataclass
from datetime import date
from typing import Any, Tuple

import requests
from dotenv import load_dotenv


def run() -> None:
    print(WeatherDataHanlder().get_weather_data())


class WeatherDataHanlder:

    load_dotenv()
    API_KEY: str = str(os.environ.get("OPENWEATHER_API_KEY"))
    API_URL: str = "http://api.openweathermap.org/data/2.5/weather?"

    def __init__(self):
        self.weather_data: dict[str, Any] = self._fetch_weather_data()
        self.today: date = date.today()

    def _fetch_weather_data(self) -> dict[str, Any]:
        target_url: str = (
            self.API_URL
            + "lat="
            + AirportLoc().LAT
            + "&lon="
            + AirportLoc().LON
            + "&units=metric"
            + "&appid="
            + self.API_KEY
        )
        try:
            response: dict[str, Any] = requests.get(target_url).json()
            return response
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except json.JSONDecodeError as err:
            raise SystemExit(err)

    def get_weather_data(self) -> dict[str, Any]:
        try:
            condition: str = self.weather_data["weather"][0].get("main", "")
            condition_description: str = self.weather_data["weather"][0].get(
                "description", ""
            )  # noqa
            temp: float = self.weather_data["main"]["temp"]
            pressure: int = self.weather_data["main"]["pressure"]
            humidity: int = self.weather_data["main"]["humidity"]
            visibility: int = self.weather_data["visibility"]
            wind_speed: float = self._get_wind_data()[0]
            wind_direction: int = self._get_wind_data()[1]
            cloudiness: int = self._get_clouds_data()
            rain: float = self._get_rain_data()
            snow: float = self._get_snow_data()
            is_dark: bool = self._is_dark()
            timestamp: int = self.weather_data["dt"]
        except KeyError:
            raise
        return Weather(
            condition=condition,
            condition_description=condition_description,
            temp=temp,
            pressure=pressure,
            humidity=humidity,
            visibility=visibility,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            cloudiness=cloudiness,
            rain=rain,
            snow=snow,
            is_dark=is_dark,
            timestamp=timestamp,
        ).as_dict()

    def _get_wind_data(self) -> Tuple[float, int]:
        wind_speed: float = 0
        wind_direction: int = -1
        if self.weather_data.get("wind") is not None:
            wind_speed = self.weather_data["wind"].get("speed", 0)
            wind_direction = self.weather_data["wind"].get("deg", -1)
        return wind_speed, wind_direction

    def _get_clouds_data(self) -> int:
        cloudiness: int = 0
        if self.weather_data.get("clouds") is not None:
            cloudiness = self.weather_data["clouds"].get("all", 0)
        return cloudiness

    def _get_rain_data(self) -> float:
        rain: float = 0
        if self.weather_data.get("rain") is not None:
            rain = self.weather_data["rain"].get("1h", 0)
        return rain

    def _get_snow_data(self) -> float:
        rain: float = 0
        if self.weather_data.get("snow") is not None:
            rain = self.weather_data["snow"].get("1h", 0)
        return rain

    def _is_dark(self) -> bool:
        try:
            timestamp: int = self.weather_data["dt"]
            sunrise: int = self.weather_data["sys"]["sunrise"]
            sunset: int = self.weather_data["sys"]["sunset"]
        except KeyError:
            raise
        return sunrise >= timestamp >= sunset


@dataclass
class Weather:
    condition: str
    condition_description: str
    temp: float
    pressure: int
    humidity: int
    visibility: int
    wind_speed: float
    wind_direction: int
    cloudiness: int
    rain: float
    snow: float
    is_dark: bool
    timestamp: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AirportLoc:
    LAT: str = "51.95763674245107"
    LON: str = "4.442139576041504"
    ZIP_CODE: str = "3045AP"
    COUNTRY: str = "NL"


if __name__ == "__main__":
    run()
