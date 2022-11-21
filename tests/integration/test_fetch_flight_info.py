import pytest

from src.data_pull.flights.fetch_flights import FlightDataHandler

TARGET_URL = "https://www.rotterdamthehagueairport.nl/wp-content/themes/rtha-v2/flights.php?updated=0"  # noqa


@pytest.fixture
def get_request():
    return FlightDataHandler().fetch_flight_info()


def test_response_is_not_null(get_request):
    print(get_request)
    assert get_request is not None


# @pytest.mark.parametrize(
#     ("key"),
#     [
#         ("arrivals"),
#         ("flightID"),
#         ("flightPORT"),
#         ("flightFLT"),
#         ("flightIATA_PORT"),
#         ("flightAIRLINE_NAME"),
#         ("flightSTATUS"),
#         ("flightARRIVALHALLS"),
#         ("flightBELTS"),
#         ("flightSCHED_DATE"),
#         ("flightSCHED_TIME"),
#         ("flightSTATUS_TIME"),
#     ],
# )
# def test_response_correct_dict_keys_present_arrivals(json_response, key):
#     if key in json_response:
#         assert True


# @pytest.mark.parametrize(
#     ("key"),
#     [
#         ("departures"),
#         ("flightID"),
#         ("flightPORT"),
#         ("flightFLT"),
#         ("flightIATA_PORT"),
#         ("flightAIRLINE_NAME"),
#         ("flightGATE"),
#         ("flightDESKS"),
#         ("flightSTATUS"),
#         ("flightSCHED_DATE"),
#         ("flightSCHED_TIME"),
#         ("flightSTATUS_TIME"),
#     ],
# )
# def test_response_correct_dict_keys_present_departures(json_response, key):
#     if key in json_response:
#         assert True
