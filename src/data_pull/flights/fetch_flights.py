import json
import urllib.request
from typing import Any

import boto3

TARGET_URL: str = "https://www.rotterdamthehagueairport.nl/wp-content/themes/rtha-v2/flights.php?updated=0"  # noqa


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    json_response = json.dumps(fetch_flight_info()).encode("UTF-8")
    s3.put_object(
        Bucket="wvane.flight-info", Key="flight-info.json", Body=bytes(json_response)
    )
    return json_response


def fetch_flight_info() -> dict[str, Any]:
    try:
        response: str = urllib.request.urlopen(TARGET_URL).read()
        response = remove_string_tails(response)
        return json.loads(response)
    except json.JSONDecodeError as err:
        raise SystemExit(err)


def remove_string_tails(string: str) -> str:
    """
    Helper function to remove the first and last character of a string.

    Implemented to remove brackets from the get request response so that
    the response can be succesfully decoded to json.
    """
    return string[1:-1]
