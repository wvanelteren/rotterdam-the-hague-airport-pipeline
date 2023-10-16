import json
import os
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Any, Tuple

import boto3

from src.utils.exceptions import NoAPIResultFetchedError
from src.utils.logger import logger

API_URL: str = "http://api.openweathermap.org/data/2.5/weather?"

def lambda_handler(event, context):
    api_key: str = os.environ["OPENWEATHER_API_KEY"]
    bucket_name = os.environ['BUCKET_NAME']
    weather_data_handler = OpenWeatherDataHandler(api_key=api_key)
    s3 = boto3.client("s3")

    weather_data_handler.fetch_weather_data(target_url=API_URL)
    weather: Weather = weather_data_handler.get_weather_data()
    weather_json = json.dumps([asdict(weather)], separators=(",", ":")).encode("utf-8")

    s3.put_object(
        Bucket=bucket_name,
        Key=current_datetime_to_string() + ".json",
        Body=bytes(weather_json),
    )
    logger.debug(f"Uploaded weather data to S3 bucket {bucket_name}")
    return weather_json


def current_datetime_to_string() -> str:
    current_time: date = datetime.now()
    return current_time.strftime("%Y/%m/%d/%H.%M")


@dataclass
class Weather:
    condition: str
    condition_description: str
    temp: float
    pressure: int
    humidity: int
    visibility: int
    wind_speed: float
    wind_direction: int | None
    cloudiness: int
    rain: float
    snow: float
    is_dark: bool
    timestamp: int

@dataclass(frozen=True)
class AirportLoc:
    LAT: str = "51.95763674245107"
    LON: str = "4.442139576041504"
    ZIP_CODE: str = "3045AP"
    COUNTRY: str = "NL"


class OpenWeatherDataHandler:
    def __init__(self, API_key: str):
        self.api_key: str = API_key
        self.weather_data: dict[str, Any] = {}

    def fetch_weather_data(self, target_url: str) -> dict[str, Any]:
        """
        Fetch weather data from the OpenWeather API and store it in the class.

        Args:
            target_url: The URL to fetch weather data from.

        Returns:
            A dictionary containing the fetched weather data.
        """
        target_url: str = (
            API_URL
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
            self.weather_data = json.loads(response)
        except urllib.error.HTTPError as err:
            logger.error(f"Cannot fetch weather data due to HTTP error: {err}")
            raise
        except json.JSONDecodeError as err:
            logger.error(f"Cannot fetch weather data due to inconsistent data format: {err}")
            raise

    def get_weather_data(self) -> dict[str, Any]:
        """
        Get and format weather data.

        Returns:
            A Weather dataclass object containing weather information.
        """
        if not self.weather_data:
            raise NoAPIResultFetchedError()
        condition: str = self.weather_data["weather"][0].get("main", "")
        condition_description: str = self.weather_data["weather"][0].get("description", "")
        temp: float = self.weather_data["main"]["temp"]
        pressure: int = self.weather_data["main"]["pressure"]
        humidity: int = self.weather_data["main"]["humidity"]
        visibility: int = self.weather_data["visibility"]
        wind_speed, wind_direction = self._get_wind_data()
        cloudiness: int = self._get_clouds_data()
        rain: float = self._get_rain_data()
        snow: float = self._get_snow_data()
        is_dark: bool = self._is_dark()
        timestamp: int = self.weather_data["dt"]
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
        )

    def _get_wind_data(self) -> Tuple[float, None|int]:
        """Get wind speed and direction"""
        wind_speed: float = 0.0
        wind_direction = None
        if self.weather_data.get("wind") is not None:
            wind_speed = self.weather_data["wind"].get("speed", 0.0)
            wind_direction = self.weather_data["wind"].get("deg", None)
        return wind_speed, wind_direction

    def _get_clouds_data(self) -> int:
        """Get cloudiness data as percentage."""
        cloudiness: int = 0
        if self.weather_data.get("clouds") is not None:
            cloudiness = self.weather_data["clouds"].get("all", 0)
        return cloudiness

    def _get_rain_data(self) -> float:
        """Get rain data as millimeter rain fallen in the last hour"""
        rain: float = 0.0
        if self.weather_data.get("rain") is not None:
            rain = self.weather_data["rain"].get("1h", 0.0)
        return rain

    def _get_snow_data(self) -> float:
        """Get snow data as centimeter snow fallen in the last hour"""
        snow: float = 0.0
        if self.weather_data.get("snow") is not None:
            snow = self.weather_data["snow"].get("1h", 0.0)
        return snow

    def _is_dark(self) -> bool:
        """Check if it is currently dark based"""
        timestamp: int = self.weather_data["dt"]
        sunrise: int = self.weather_data["sys"]["sunrise"]
        sunset: int = self.weather_data["sys"]["sunset"]
        return not sunrise <= timestamp <= sunset
