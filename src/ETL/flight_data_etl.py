from datetime import date

import awswrangler as wr


def run_ETL() -> None:
    arrivals_ETL()
    departures_ETL()


def arrivals_ETL() -> None:
    arrivals = Extractor().extract_arrivals()
    transformed_arrivals = Transformer(arrivals).transform()
    Loader(transformed_arrivals).arrivals_to_csv()


def departures_ETL() -> None:
    departures = Extractor().extract_departures()
    transformed_departures = Transformer(departures).transform()
    Loader(transformed_departures).departures_to_csv()


class Extractor:
    today: date = date.today()
    day: str = today.strftime("%d")
    month: str = today.strftime("%m")
    year: str = today.strftime("%Y")

    BUCKET: str = "wvane.flight-data-raw"
    FLIGHT_DATA_ARRIVALS_PATH: str = f"s3://{BUCKET}/arrivals/{year}/{month}/{day}/"
    FLIGHT_DATA_DEPARTURES_PATH: str = f"s3://{BUCKET}/departures/{year}/{month}/{day}/"

    def extract_arrivals(self, path: str = FLIGHT_DATA_ARRIVALS_PATH):
        return self._read_all_json_files_from_path(path=path)

    def extract_departures(self, path: str = FLIGHT_DATA_DEPARTURES_PATH):
        return self._read_all_json_files_from_path(path=path)

    def _read_all_json_files_from_path(self, path: str):
        return wr.s3.read_json(path=path, path_suffix=".json")


class Transformer:
    def __init__(self, df):
        self.df = df

    def transform(self):
        self._change_badgeid_column_to_timestamp()
        self._deduplicate_keep_entry_with_latest_timestamp()
        return self.df

    def _change_badgeid_column_to_timestamp(self) -> None:
        try:
            self.df.rename(columns={"badge_id": "timestamp"}, inplace=True)
        except KeyError:
            raise

    def _deduplicate_keep_entry_with_latest_timestamp(self) -> None:
        try:
            self.df = self.df.sort_values("timestamp").drop_duplicates(
                ["flightID"], keep="last"
            )
        except KeyError:
            raise


class Loader:
    today: date = date.today()
    filename: str = today.strftime("%Y-%m-%d")

    TARGET_PATH_ARRIVALS: str = "s3://wvane.flight-data-clean/arrivals/" + filename
    TARGET_PATH_DEPARTURES: str = "s3://wvane.flight-data-clean/departures/" + filename

    def __init__(self, df):
        self.df = df

    def arrivals_to_csv(self) -> None:
        target_path: str = self.TARGET_PATH_ARRIVALS + ".csv"
        wr.s3.to_csv(self.df, target_path, index=False)

    def departures_to_csv(self) -> None:
        target_path: str = self.TARGET_PATH_DEPARTURES + ".csv"
        wr.s3.to_csv(self.df, target_path, index=False)

    def arrivals_to_parquet(self) -> None:
        target_path: str = self.TARGET_PATH_ARRIVALS + ".parquet"
        wr.s3.to_parquet(self.df, target_path, index=False)

    def departures_to_parquet(self) -> None:
        target_path: str = self.TARGET_PATH_DEPARTURES + ".parquet"
        wr.s3.to_parquet(self.df, target_path, index=False)


if __name__ == "__main__":
    run_ETL()
