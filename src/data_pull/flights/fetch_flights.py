import json
import os
import urllib.error
import urllib.request
from datetime import date, datetime
from typing import Any

import boto3

from src.utils.exceptions import NoAPIResultFetchedError
from src.utils.logger import logger

# The target URL for fetching flight data
TARGET_URL: str = "https://www.rotterdamthehagueairport.nl/wp-content/themes/rtha-v2/flights.php?updated=0"


def lambda_handler(event, context):
    """
    Lambda function entry point for fetching flight data and saving it in S3.

    Args:
        event: AWS Lambda event data
        context: AWS Lambda context

    Returns:
        A list containing arrivals and departures data (for debug purposes only)
    """
    flight_data_handler = FlightDataHandler()
    bucket_name = os.environ["BUCKET_NAME"]
    s3 = boto3.client("s3")

    flight_data_handler.fetch_flight_data(target_url=TARGET_URL)
    arrivals: list[dict[str, str]] = flight_data_handler.get_arrivals_today()
    departures: list[dict[str, str]] = flight_data_handler.get_departures_today()

    arrivals_json = json.dumps(arrivals, separators=(",", ":")).encode("utf-8")
    departures_json = json.dumps(departures, separators=(",", ":")).encode("utf-8")

    s3.put_object(
        Bucket=bucket_name,
        Key="arrivals/" + current_datetime_to_string() + ".json",
        Body=bytes(arrivals_json),
    )
    s3.put_object(
        Bucket=bucket_name,
        Key="departures/" + current_datetime_to_string() + ".json",
        Body=bytes(departures_json),
    )
    logger.debug(f"uploaded flight data to S3 bucket {bucket_name}")
    return arrivals + departures


def current_datetime_to_string() -> str:
    """
    Convert the current datetime to a formatted string.

    Returns:
        A string representing the current datetime in the format "YYYY/MM/DD/HH.MM"
    """
    current_time: date = datetime.now()
    return current_time.strftime("%Y/%m/%d/%H.%M")


class FlightDataHandler:
    def __init__(self):
        self.flight_data: dict[str, Any] = {}
        self.today: date = date.today()

    def fetch_flight_data(self, target_url: str) -> dict[str, Any]:
        """
        Fetch flight data from a specified URL and store it in the class.

        Args:
            target_url: The URL to fetch flight data from.

        Returns:
            A dictionary containing the fetched flight data.
        """
        try:
            response = urllib.request.Request(target_url)
            with urllib.request.urlopen(response) as response:
                response: str = response.read()
            response: str = self.remove_string_tails(response)
            self.flight_data = json.loads(response)
        except urllib.error.HTTPError:
            logger.exception("Cannot fetch weather data due to HTTP error")
            raise
        except json.JSONDecodeError:
            logger.exception("Cannot fetch flight data due to inconsistent data format")
            raise

    def get_arrivals_today(self) -> list[dict[str, str]]:
        """Get the list of arrivals for the current date."""
        return self._get_flights_today(key="arrivals")

    def get_departures_today(self) -> list[dict[str, str]]:
        """Get the list of departures for the current date."""
        return self._get_flights_today(key="departures")

    def _get_flights_today(self, key: str) -> list[dict[str, str]]:
        """
        Get the list of flights (arrivals or departures) for the current date.

        Args:
            key: A string specifying whether to get arrivals or departures.

        Returns:
            A list of dictionaries containing flight data for the current date.
        """
        if not self.flight_data:
            raise NoAPIResultFetchedError()
        flights: list[dict[str, str]] = []
        today: str = self.today.strftime("%Y-%m-%d")
        for flight in self.flight_data["flights"][key][today]:
            flights.append(flight)
        return flights

    @staticmethod
    def remove_string_tails(string: str) -> str:
        """
        Helper function to remove the first and last character of a string.

        Implemented to remove brackets from the get request response so that
        the response can be succesfully decoded to json.
        """
        return string[1:-1]
