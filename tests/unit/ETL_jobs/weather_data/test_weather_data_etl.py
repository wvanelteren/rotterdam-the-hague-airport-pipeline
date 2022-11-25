import pandas as pd
import pytest

# from tabulate import tabulate


@pytest.fixture
def load_merged_data():
    weather_df_1 = pd.read_json("tests/unit/ETL_jobs/weather_data/weather_data_1.json")
    weather_df_2 = pd.read_json("tests/unit/ETL_jobs/weather_data/weather_data_2.json")
    return pd.concat([weather_df_1, weather_df_2], axis=0, ignore_index=True)


def test_change_timestamp_from_unix_to_datetime(load_merged_data):
    df = load_merged_data
    print(df)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, unit="s")  # type: ignore # noqa
    print(df["timestamp"])
    df.to_csv("output2.csv", index=False)
    assert True
