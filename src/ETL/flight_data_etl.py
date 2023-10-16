from datetime import date

import awswrangler as wr


def run_ETL() -> None:
    arrivals_ETL()
    departures_ETL()


def arrivals_ETL() -> None:
    arrivals = Extractor().extract_arrivals()
    transformed_arrivals = Transformer(arrivals).transform()
    Loader(transformed_arrivals).arrivals_to_parquet()


def departures_ETL() -> None:
    departures = Extractor().extract_departures()
    transformed_departures = Transformer(departures).transform()
    Loader(transformed_departures).departures_to_parquet()


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
        self._change_badgeid_column_to_timestamp_crawled()
        self._deduplicate_keep_entry_with_latest_timestamp()
        self._create_column_difference_sched_and_status_time_in_minutes()
        self._create_column_is_delayed()
        return self.df

    def _change_badgeid_column_to_timestamp_crawled(self) -> None:
        try:
            self.df.rename(columns={"badge_id": "timestamp_crawled"}, inplace=True)
        except KeyError:
            raise

    def _deduplicate_keep_entry_with_latest_timestamp(self) -> None:
        try:
            self.df = self.df.sort_values("timestamp_crawled").drop_duplicates(["flightID"], keep="last")
        except KeyError:
            raise

    def _create_column_difference_sched_and_status_time_in_minutes(self) -> None:
        try:
            self.df["flightDIFF_TIME"] = (self.df["flightSTATUS_TIME"] - self.df["flightSCHED_TIME"]).map(
                lambda x: x.total_seconds() / 60
            )
        except KeyError:
            raise

    def _create_column_is_delayed(self) -> None:
        self.df["flightIS_DELAYED"] = self.df["flightDIFF_TIME"] > 15


class Loader:
    today: date = date.today()
    filename: str = today.strftime("%Y-%m-%d")

    TARGET_PATH_ARRIVALS: str = "s3://wvane.flight-data-clean/"
    TARGET_PATH_DEPARTURES: str = "s3://wvane.flight-data-clean/"

    def __init__(self, df):
        self.df = df

    def arrivals_to_csv(self, path: str = TARGET_PATH_ARRIVALS, filename: str = filename) -> None:
        target_path: str = path + "arrivals_csv/" + filename + ".csv"
        wr.s3.to_csv(self.df, target_path, index=False)

    def departures_to_csv(self, path: str = TARGET_PATH_DEPARTURES, filename: str = filename) -> None:
        target_path: str = path + "departures_csv/" + filename + ".csv"
        wr.s3.to_csv(self.df, target_path, index=False)

    def arrivals_to_parquet(self, path: str = TARGET_PATH_ARRIVALS) -> None:
        target_path: str = path + "arrivals.parquet"
        wr.s3.to_parquet(df=self.df, path=target_path, dataset=True, mode="append")

    def departures_to_parquet(self, path: str = TARGET_PATH_DEPARTURES) -> None:
        target_path: str = path + "departures.parquet"
        wr.s3.to_parquet(df=self.df, path=target_path, dataset=True, mode="append")


if __name__ == "__main__":
    run_ETL()
