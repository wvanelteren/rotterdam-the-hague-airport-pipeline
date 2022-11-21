import json
import urllib.request
from datetime import datetime
from typing import Any

import boto3


def lambda_handler(event, context):
    flight_data_handler = FlightDataHandler()
    s3 = boto3.client("s3")

    response: dict[str, Any] = flight_data_handler.fetch_flight_info()
    arrivals: list[dict[str, str]] = flight_data_handler.get_arrivals(response)
    departures: list[dict[str, str]] = flight_data_handler.get_departures(response)

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
    return {"arrivals": [arrivals_json], "departures": [departures_json]}


def current_datetime_to_string() -> str:
    current_time = datetime.now()
    return current_time.strftime("%Y/%m/%d/%H.%M")


class FlightDataHandler:
    TARGET_URL: str = "https://www.rotterdamthehagueairport.nl/wp-content/themes/rtha-v2/flights.php?updated=0"  # noqa

    def fetch_flight_info(self) -> dict[str, Any]:
        try:
            response: str = urllib.request.urlopen(self.TARGET_URL).read()
            response = self.remove_string_tails(response)
            return json.loads(response)
        except json.JSONDecodeError as err:
            raise SystemExit(err)

    def get_arrivals(self, response: dict[str, Any]) -> list[dict[str, str]]:
        arrivals: list[dict[str, str]] = []
        for flights in list(response["flights"]["arrivals"].values())[0]:
            arrivals.append(flights)
        for flights in list(response["flights"]["arrivals"].values())[1]:
            arrivals.append(flights)
        return arrivals

    def get_departures(self, response: dict[str, Any]) -> list[dict[str, str]]:
        departures: list[dict[str, str]] = []
        for flights in list(response["flights"]["departures"].values())[0]:
            departures.append(flights)
        for flights in list(response["flights"]["departures"].values())[1]:
            departures.append(flights)
        return departures

    @staticmethod
    def remove_string_tails(string: str) -> str:
        """
        Helper function to remove the first and last character of a string.

        Implemented to remove brackets from the get request response so that
        the response can be succesfully decoded to json.
        """
        return string[1:-1]
