from datetime import date

import awswrangler as wr
import pandas as pd


def run_ETL() -> None:
    weather_data = Extractor().extract()
    transformed_weather_data = Transformer(weather_data).transform()
    Loader(transformed_weather_data).to_csv()


class Extractor:
    today: date = date.today()
    day: str = today.strftime("%d")
    month: str = today.strftime("%m")
    year: str = today.strftime("%Y")

    BUCKET: str = "wvane.weather-data-raw"
    WEATHER_DATA_PATH: str = f"s3://{BUCKET}/{year}/{month}/{day}/"

    def extract(self, path: str = WEATHER_DATA_PATH):
        return self._read_all_json_files_from_path(path=path)

    def _read_all_json_files_from_path(self, path: str):
        return wr.s3.read_json(path=path, path_suffix=".json")


class Transformer:
    def __init__(self, df):
        self.df = df

    def transform(self):
        self._sort_by_timestamp()
        self._deduplicate_same_timestamp()
        self._change_timestamp_from_unix_to_datetime()
        return self.df

    def _sort_by_timestamp(self) -> None:
        self.df = self.df.sort_values("timestamp")

    def _deduplicate_same_timestamp(self) -> None:
        self.df = self.df.drop_duplicates("timestamp")

    def _change_timestamp_from_unix_to_datetime(self) -> None:
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"], unit="s")


class Loader:
    today: date = date.today()
    filename: str = today.strftime("%Y-%m-%d")

    TARGET_PATH: str = "s3://wvane.weather-data-clean/" + filename

    def __init__(self, df):
        self.df = df

    def to_csv(self, path: str = TARGET_PATH) -> None:
        target_path: str = path + ".csv"
        wr.s3.to_csv(self.df, target_path, index=False)

    def to_parquet(self, path: str = TARGET_PATH) -> None:
        target_path: str = path + ".parquet"
        wr.s3.to_parquet(self.df, target_path, index=False)


if __name__ == "__main__":
    run_ETL()
