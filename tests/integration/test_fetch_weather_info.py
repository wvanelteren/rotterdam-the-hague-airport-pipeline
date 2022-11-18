from src.data_pull.weather.fetch_weather import fetch_weather_info


def test_airport_weather_response():
    response = fetch_weather_info()
    print(response)
    assert len(response) != 0
