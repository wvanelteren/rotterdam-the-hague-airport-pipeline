import json

import pytest

from src.data_pull.flights.fetch_flights import remove_string_tails


@pytest.fixture
def api_response():
    with open("tests/unit/response.text", encoding="utf-8") as response:
        return response.read()


def test_response_decodes_to_json_succesfully(api_response):
    try:
        response = api_response[1:-1]
        json.loads(response)
    except json.JSONDecodeError:
        assert False


def test_string_tails_remover():
    string = "hello world"
    assert remove_string_tails(string) == "ello worl"
