import json
from datetime import date

import pytest
from mock import patch

from src.data_pull.flights.fetch_flights import FlightDataHandler


@pytest.fixture
def MockFlightData(flight_data):
    def __init__(self):
        self.flight_data = json.loads(flight_data[1:-1])
        self.today = date(year=2022, month=11, day=17)

    with patch.object(FlightDataHandler, "__init__", __init__):
        yield FlightDataHandler()


def test_response_decodes_to_json_succesfully(flight_data):
    try:
        json.loads(flight_data[1:-1])
    except json.JSONDecodeError:
        assert False


def test_string_tails_remover():
    string = "hello world"
    assert FlightDataHandler().remove_string_tails(string) == "ello worl"


def test_print_today(MockFlightData):
    assert MockFlightData._print_date_today() == "2022-11-17"


def test_get_arrivals_today(MockFlightData):
    print(MockFlightData.get_arrivals_today())
    assert MockFlightData.get_arrivals_today() is not None


def test_get_departures_today(MockFlightData):
    print(MockFlightData.get_departures_today())
    assert MockFlightData.get_departures_today() is not None


def test_get_flight_data_today(MockFlightData):
    key = "arrivals"
    flights: list[dict[str, str]] = []
    today = MockFlightData._print_date_today()
    try:
        for flight in MockFlightData.flight_data["flights"][key][today]:
            flights.append(flight)
            assert True
    except KeyError:
        assert False


@pytest.fixture
def flight_data():
    return """({
    "flights": {
        "arrivals": {
            "2022-11-17": [
                {
                    "badge_id": "1668694531",
                    "flightID": "S436528",
                    "flightFLT": "HV5244 ",
                    "flightPORT": "Lissabon",
                    "flightIATA_PORT": "LIS",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightSTATUS": "IN BLOCK",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "13:50",
                    "flightSTATUS_TIME": "14:10"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S436577",
                    "flightFLT": "HV6094 ",
                    "flightPORT": "Faro",
                    "flightIATA_PORT": "FAO",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightSTATUS": "IN BLOCK",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "14:00",
                    "flightSTATUS_TIME": "13:42"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S436859",
                    "flightFLT": "BA4455 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightSTATUS": "IN BLOCK",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "14:30",
                    "flightSTATUS_TIME": "14:22"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S437904",
                    "flightFLT": "HV6064 ",
                    "flightPORT": "Barcelona",
                    "flightIATA_PORT": "BCN",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "17:45"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438068",
                    "flightFLT": "BA4457 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "18:25"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S439360",
                    "flightFLT": "OR1693 ",
                    "flightPORT": "Tenerife",
                    "flightVIA": "Arrecife",
                    "flightIATA_PORT": "TFS",
                    "flightAIRLINE_NAME": "TUI fly Nederland",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "20:45"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438572",
                    "flightFLT": "BA4459 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "21:30"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438774",
                    "flightFLT": "HV6962 ",
                    "flightPORT": "Edinburgh",
                    "flightIATA_PORT": "EDI",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "22:10"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438960",
                    "flightFLT": "HV5592 ",
                    "flightPORT": "Al-hoceima",
                    "flightIATA_PORT": "AHU",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "22:20"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S439128",
                    "flightFLT": "HV5024 ",
                    "flightPORT": "Malaga",
                    "flightIATA_PORT": "AGP",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "22:35"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S439251",
                    "flightFLT": "HV5052 ",
                    "flightPORT": "Alicante",
                    "flightIATA_PORT": "ALC",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "22:45"
                }
            ],
            "2022-11-18": [
                {
                    "badge_id": "1668694531",
                    "flightID": "S435283",
                    "flightFLT": "BA4451 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "09:30"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S435537",
                    "flightFLT": "TB7065 ",
                    "flightPORT": "Oujda",
                    "flightIATA_PORT": "OUD",
                    "flightAIRLINE_NAME": "TUI fly Belgium",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "10:30"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S436112",
                    "flightFLT": "HV6038 ",
                    "flightPORT": "Rome - Fiumicino",
                    "flightIATA_PORT": "FCO",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "12:40"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S436276",
                    "flightFLT": "HV5052 ",
                    "flightPORT": "Alicante",
                    "flightIATA_PORT": "ALC",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "12:55"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S436381",
                    "flightFLT": "PC1261 ",
                    "flightPORT": "Istanbul - Sabiha G.",
                    "flightIATA_PORT": "SAW",
                    "flightAIRLINE_NAME": "Pegasus",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "13:25"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S436644",
                    "flightFLT": "HV5022 ",
                    "flightPORT": "Malaga",
                    "flightIATA_PORT": "AGP",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "14:05"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S436895",
                    "flightFLT": "HV5702 ",
                    "flightPORT": "Tanger",
                    "flightIATA_PORT": "TNG",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "14:30"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S436877",
                    "flightFLT": "BA4455 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "14:30"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S437642",
                    "flightFLT": "HV6302 ",
                    "flightPORT": "Gran Canaria",
                    "flightIATA_PORT": "LPA",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "16:45"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S437862",
                    "flightFLT": "HV6082 ",
                    "flightPORT": "Bergerac",
                    "flightIATA_PORT": "EGC",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "17:40"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438089",
                    "flightFLT": "BA4457 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "18:25"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438348",
                    "flightFLT": "TB7061 ",
                    "flightPORT": "Marrakech",
                    "flightIATA_PORT": "RAK",
                    "flightAIRLINE_NAME": "TUI fly Belgium",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "19:20"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438593",
                    "flightFLT": "BA4459 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "21:30"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S439364",
                    "flightFLT": "OR1617 ",
                    "flightPORT": "Fuerteventura",
                    "flightVIA": "Gran Canaria",
                    "flightIATA_PORT": "FUE",
                    "flightAIRLINE_NAME": "TUI fly Nederland",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "2",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "21:30"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438699",
                    "flightFLT": "HV6442 ",
                    "flightPORT": "Valencia",
                    "flightIATA_PORT": "VLC",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "22:00"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S439063",
                    "flightFLT": "HV5596 ",
                    "flightPORT": "Nador",
                    "flightIATA_PORT": "NDR",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "22:30"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S439098",
                    "flightFLT": "HV6094 ",
                    "flightPORT": "Faro",
                    "flightIATA_PORT": "FAO",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "22:30"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S439227",
                    "flightFLT": "HV6064 ",
                    "flightPORT": "Barcelona",
                    "flightIATA_PORT": "BCN",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightARRIVALHALLS": "1",
                    "flightBELTS": "1",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "22:40"
                }
            ]
        },
        "departures": {
            "2022-11-17": [
                {
                    "badge_id": "1668694531",
                    "flightID": "S437069",
                    "flightFLT": "BA4456 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightGATE": "08",
                    "flightDESKS": "02-03",
                    "flightSTATUS": "DEPARTED",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "15:05",
                    "flightSTATUS_TIME": "15:11"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S439474",
                    "flightFLT": "HV5591 ",
                    "flightPORT": "Al-hoceima",
                    "flightIATA_PORT": "AHU",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightGATE": "11",
                    "flightSTATUS": "BOARDING",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "15:20"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S437409",
                    "flightFLT": "HV5023 ",
                    "flightPORT": "Malaga",
                    "flightIATA_PORT": "AGP",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightGATE": "02",
                    "flightDESKS": "12-13",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "16:00"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S437743",
                    "flightFLT": "HV5051 ",
                    "flightPORT": "Alicante",
                    "flightIATA_PORT": "ALC",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightGATE": "06",
                    "flightDESKS": "11",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "16:55"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438181",
                    "flightFLT": "HV6961 ",
                    "flightPORT": "Edinburgh",
                    "flightIATA_PORT": "EDI",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightGATE": "10",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "18:45"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438296",
                    "flightFLT": "BA4458 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightGATE": "07",
                    "flightSCHED_DATE": "2022-11-17",
                    "flightSCHED_TIME": "19:00"
                }
            ],
            "2022-11-18": [
                {
                    "badge_id": "1668694531",
                    "flightID": "S434283",
                    "flightFLT": "HV6301 ",
                    "flightPORT": "Gran Canaria",
                    "flightIATA_PORT": "LPA",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightGATE": "03",
                    "flightDESKS": "15-16",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "06:55"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S434617",
                    "flightFLT": "HV5051 ",
                    "flightPORT": "Alicante",
                    "flightIATA_PORT": "ALC",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightGATE": "01",
                    "flightDESKS": "13-14",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "07:10"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S434783",
                    "flightFLT": "HV6037 ",
                    "flightPORT": "Rome - Fiumicino",
                    "flightIATA_PORT": "FCO",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightGATE": "04",
                    "flightDESKS": "11-12",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "07:20"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S434869",
                    "flightFLT": "HV5021 ",
                    "flightPORT": "Malaga",
                    "flightIATA_PORT": "AGP",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightGATE": "08",
                    "flightDESKS": "09-10",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "07:30"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S435006",
                    "flightFLT": "HV5701 ",
                    "flightPORT": "Tanger",
                    "flightIATA_PORT": "TNG",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightGATE": "11",
                    "flightDESKS": "06-08",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "07:35"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S435385",
                    "flightFLT": "BA4452 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightGATE": "10",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "10:05"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S439371",
                    "flightFLT": "OR1617 ",
                    "flightPORT": "Gran Canaria",
                    "flightVIA": "Fuerteventura",
                    "flightIATA_PORT": "LPA",
                    "flightAIRLINE_NAME": "TUI fly Nederland",
                    "flightGATE": "02",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "10:05"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S435558",
                    "flightFLT": "BA4450 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightGATE": "11",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "10:40"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S435829",
                    "flightFLT": "TB7066 ",
                    "flightPORT": "Oujda",
                    "flightIATA_PORT": "OUD",
                    "flightAIRLINE_NAME": "TUI fly Belgium",
                    "flightGATE": "07",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "11:25"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S436557",
                    "flightFLT": "HV6081 ",
                    "flightPORT": "Bergerac",
                    "flightIATA_PORT": "EGC",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "13:55"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S436748",
                    "flightFLT": "PC1262 ",
                    "flightPORT": "Istanbul - Sabiha G.",
                    "flightIATA_PORT": "SAW",
                    "flightAIRLINE_NAME": "Pegasus",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "14:10"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S437087",
                    "flightFLT": "BA4456 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "15:05"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S437269",
                    "flightFLT": "HV5595 ",
                    "flightPORT": "Nador",
                    "flightIATA_PORT": "NDR",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "15:40"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S437335",
                    "flightFLT": "HV6093 ",
                    "flightPORT": "Faro",
                    "flightIATA_PORT": "FAO",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "15:45"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S437560",
                    "flightFLT": "HV6441 ",
                    "flightPORT": "Valencia",
                    "flightIATA_PORT": "VLC",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "16:35"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S437850",
                    "flightFLT": "HV6063 ",
                    "flightPORT": "Barcelona",
                    "flightIATA_PORT": "BCN",
                    "flightAIRLINE_NAME": "Transavia",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "17:40"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438317",
                    "flightFLT": "BA4458 ",
                    "flightPORT": "London City",
                    "flightIATA_PORT": "LCY",
                    "flightAIRLINE_NAME": "British Airways",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "19:00"
                },
                {
                    "badge_id": "1668694531",
                    "flightID": "S438386",
                    "flightFLT": "TB7062 ",
                    "flightPORT": "Marrakech",
                    "flightIATA_PORT": "RAK",
                    "flightAIRLINE_NAME": "TUI fly Belgium",
                    "flightSCHED_DATE": "2022-11-18",
                    "flightSCHED_TIME": "20:15"
                }
            ]
        }
    },
    "updated": "1668694531"
})"""
