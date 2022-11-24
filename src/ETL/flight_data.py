from datetime import date

import awswrangler as wr

today: date = date.today()
day: str = today.strftime("%d")
month: str = today.strftime("%m")
year: str = today.strftime("%Y")

FLIGHT_DATA_ARRIVALS_PATH: str = (
    f"s3://wvane.flight-data-raw/arrivals/{year}/{month}/{day}/"  # noqa
)
FLIGHT_DATA_DEPARTURES_PATH: str = (
    f"s3://wvane.flight-data-raw/departures/{year}/{month}/{day}/"  # noqa
)

TARGET_PATH: str = (
    f"s3://wvane.flight-data-clean/arrivals/{year}/{month}/{day}/"  # noqa
)

arrivals_df = wr.s3.read_json(path=FLIGHT_DATA_ARRIVALS_PATH, path_suffix=".json")
wr.s3.to_csv(arrivals_df, TARGET_PATH, index=False)
