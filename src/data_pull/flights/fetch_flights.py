import json
import urllib.request
from datetime import date, datetime
from typing import Any

import boto3


def lambda_handler(event, context):
    flight_data_handler = FlightDataHandler()
    s3 = boto3.client("s3")

    arrivals: list[dict[str, str]] = flight_data_handler.get_arrivals_today()
    departures: list[dict[str, str]] = flight_data_handler.get_departures_today()

    arrivals_json = json.dumps(arrivals, separators=(",", ":")).encode("utf-8")
    departures_json = json.dumps(departures, separators=(",", ":")).encode("utf-8")

    s3.put_object(
        Bucket="wvane.flight-info",
        Key="arrivals/" + current_datetime_to_string() + ".json",
        Body=bytes(arrivals_json),
    )
    s3.put_object(
        Bucket="wvane.flight-info",
        Key="departures/" + current_datetime_to_string() + ".json",
        Body=bytes(departures_json),
    )
    return arrivals + departures


def current_datetime_to_string() -> str:
    current_time: date = datetime.now()
    return current_time.strftime("%Y/%m/%d/%H.%M")


class FlightDataHandler:
    TARGET_URL: str = "https://www.rotterdamthehagueairport.nl/wp-content/themes/rtha-v2/flights.php?updated=0"  # noqa

    def __init__(self, target_url: str = TARGET_URL):
        self.flight_data: dict[str, Any] = self._fetch_flight_data(target_url)
        self.today: date = date.today()

    def _fetch_flight_data(self, target_url: str) -> dict[str, Any]:
        try:
            response: str = urllib.request.urlopen(target_url).read()
            response = self.remove_string_tails(response)
            return json.loads(response)
        except json.JSONDecodeError as err:
            raise SystemExit(err)

    def get_arrivals_today(self) -> list[dict[str, str]]:
        return self._get_flights_today(key="arrivals")

    def get_departures_today(self) -> list[dict[str, str]]:
        return self._get_flights_today(key="departures")

    def _get_flights_today(self, key: str) -> list[dict[str, str]]:
        flights: list[dict[str, str]] = []
        today: str = self._print_date_today()
        print(self.flight_data["flights"][key][today])
        try:
            for flight in self.flight_data["flights"][key][today]:
                flights.append(flight)
        except KeyError:
            raise
        return flights

    def _print_date_today(self) -> str:
        return self.today.strftime("%Y-%m-%d")

    @staticmethod
    def remove_string_tails(string: str) -> str:
        """
        Helper function to remove the first and last character of a string.

        Implemented to remove brackets from the get request response so that
        the response can be succesfully decoded to json.
        """
        return string[1:-1]
