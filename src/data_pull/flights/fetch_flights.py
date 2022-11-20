import json
from typing import Any

import requests

TARGET_URL: str = "https://www.rotterdamthehagueairport.nl/wp-content/themes/rtha-v2/flights.php?updated=0"  # noqa


def fetch_flight_info() -> dict[str, Any]:
    try:
        response: str = requests.get(TARGET_URL).text
        json_response: dict[str, Any] = json.loads(remove_string_tails(response))
        return json_response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except json.JSONDecodeError as err:
        raise SystemExit(err)


def remove_string_tails(string: str):
    """
    Helper function to remove the first and last character of a string.

    Implemented to remove brackets from the get request response so that
    the response can be succesfully decoded to json.
    """
    return string[1:-1]
