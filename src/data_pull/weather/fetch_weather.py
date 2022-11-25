import json
import os
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Any, Tuple

import boto3


def lambda_handler(event, context):
    api_key: str = os.environ["OPENWEATHER_API_KEY"]
    weather_data_handler = WeatherDataHandler(api_key=api_key)
    s3 = boto3.client("s3")

    weather = weather_data_handler.get_weather_data()

    weather_json = json.dumps(weather, separators=(",", ":")).encode("utf-8")

    s3.put_object(
        Bucket="wvane.weather-data-raw",
        Key=current_datetime_to_string() + ".json",
        Body=bytes(weather_json),
    )
    return weather_json


def current_datetime_to_string() -> str:
    current_time: date = datetime.now()
    return current_time.strftime("%Y/%m/%d/%H.%M")


class WeatherDataHandler:

    API_URL: str = "http://api.openweathermap.org/data/2.5/weather?"

    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.weather_data: dict[str, Any] = self._fetch_weather_data()

    def _fetch_weather_data(self) -> dict[str, Any]:
        target_url: str = (
            self.API_URL
            + "lat="
            + AirportLoc().LAT
            + "&lon="
            + AirportLoc().LON
            + "&units=metric"
            + "&appid="
            + self.api_key
        )
        try:
            response: str = urllib.request.urlopen(target_url).read()
            return json.loads(response)
        except urllib.error.HTTPError as err:
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
