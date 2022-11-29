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


def test_if_flight_schedule_time_is_of_datetime_type(load_merged_data):
    assert load_merged_data["flightSCHED_TIME"].dtype == "datetime64[ns]"


def test_if_flight_status_time_is_of_datetime_type(load_merged_data):
    assert load_merged_data["flightSTATUS_TIME"].dtype == "datetime64[ns]"


def test_if_duplicates_present(load_merged_data):
    assert load_merged_data["flightID"].is_unique is False


@pytest.mark.parametrize(
    ("index, expected"),
    [(0, pd.Timedelta("0 days 00:14:00")), (1, pd.Timedelta("-1 days +23:40:00"))],
)
def test_creation_new_column_difference_flight_time_scheduled_and_flight_time_status(
    load_merged_data, index, expected
):
    load_merged_data["flightDiff_TIME"] = (
        load_merged_data["flightSTATUS_TIME"] - load_merged_data["flightSCHED_TIME"]
    )
    assert load_merged_data["flightDiff_TIME"][index] == expected


@pytest.mark.parametrize(
    ("index, expected"),
    [(0, False), (1, False)],
)
def test_creation_new_column_is_delayed(load_merged_data, index, expected):
    load_merged_data["flightDiff_TIME"] = (
        load_merged_data["flightSTATUS_TIME"] - load_merged_data["flightSCHED_TIME"]
    )
    load_merged_data["flightIS_DELAYED"] = load_merged_data["flightDiff_TIME"].map(
        lambda x: True if x > pd.Timedelta(minutes=15) else False
    )
    assert load_merged_data["flightIS_DELAYED"][index] == expected  # noqa


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
