import os

from dotenv import load_dotenv

from src.data_pull.weather.fetch_weather import AirportLoc


def test_load_env_variable():
    load_dotenv()
    assert str(os.environ.get("TEST")) == "TEST"  # type: ignore


def test_url_string_concat():
    API_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "api_key"
    target_url = (
        API_URL + "lat=" + AirportLoc().LAT + "&lon=" + AirportLoc().LON + "&units=metric" + "&appid=" + API_KEY
    )
    assert (
        target_url
        == "http://api.openweathermap.org/data/2.5/weather?lat=51.95763674245107&lon=4.442139576041504&units=metric&appid=api_key"  # noqa
    )


def test_is_dark_returns_correct_bool():
    timestamp = 1669400294
    sunset = 1669390799
    sunrise = 1669360859
    assert not sunrise < timestamp < sunset is True
