import pandas as pd
import pytest

# from tabulate import tabulate


@pytest.fixture
def load_merged_data():
    departures_df_1 = pd.read_json(
        "tests/unit/ETL_jobs/flight_data/departures_data_1.json"
    )
    departures_df_2 = pd.read_json(
        "tests/unit/ETL_jobs/flight_data/departures_data_2.json"
    )
    return pd.concat([departures_df_1, departures_df_2], axis=0, ignore_index=True)


def test_if_duplicates_present(load_merged_data):
    assert load_merged_data["flightID"].is_unique is False


def test_name_change(load_merged_data):
    load_merged_data.rename(columns={"badge_id": "timestamp"}, inplace=True)
    try:
        assert "timestamp" in load_merged_data.columns
    except KeyError:
        assert False


def test_deduplicate_keep_entry_with_latest_timestamp(load_merged_data):
    df = load_merged_data.sort_values("badge_id").drop_duplicates(
        ["flightID"], keep="last"
    )
    assert df["flightID"].is_unique
