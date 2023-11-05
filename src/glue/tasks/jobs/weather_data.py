from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import DataFrame
from pyspark.sql.functions import from_unixtime, to_timestamp

import tasks


def change_schema(dyf: DynamicFrame) -> DynamicFrame:
    """
    Changes the schema of the DynamicFrame by resolving choice for temp, wind_speed, rain, and snow to double.

    Args:
        dyf: The DynamicFrame whose schema is to be changed.

    Returns:
        The DynamicFrame with the updated schema.
    """
    resolve_choice_specs = [
        ("temp", "cast:double"),
        ("wind_speed", "cast:double"),
        ("rain", "cast:double"),
        ("snow", "cast:double"),
    ]
    return dyf.resolveChoice(specs=resolve_choice_specs)


def sort_by_timestamp(df: DataFrame) -> DataFrame:
    """
    Sorts the DataFrame by the timestamp column.

    Args:
        df: The DataFrame to be sorted.

    Returns:
        A DataFrame sorted by the timestamp column.
    """
    df.createOrReplaceTempView("df")
    result_df = tasks.get_spark().sql("""
        SELECT *
        FROM df
        ORDER BY timestamp
        """)
    return result_df


def deduplicate_by_timestamp(df: DataFrame) -> DataFrame:
    """
    Removes duplicate rows from the DataFrame based on the timestamp column.

    Args:
        df: The DataFrame from which duplicates are to be removed.

    Returns:
        A DataFrame without any duplicate rows based on the timestamp column.
    """
    return df.dropDuplicates(["timestamp"])


def transform_unixtime_to_datetime(df: DataFrame) -> DataFrame:
    """
    Transforms the unix timestamp in the DataFrame to a datetime format.

    Args:
        df: The DataFrame whose unix timestamp is to be transformed.

    Returns:
        A DataFrame with the unix timestamp transformed to a datetime format.
    """
    df = df.withColumn("timestamp", from_unixtime("timestamp"))
    return df.withColumn("timestamp", to_timestamp("timestamp"))


def create_and_stage_weather_data(input_path: str, output_path: str) -> DataFrame:
    """
    Creates and stages weather data by reading from an input path, transforming the data, 
    and writing it to an output path. This path can either be a local path, S3 path or Redshift cluster

    Args:
        input_path: The path to read the input data from.
        output_path: The path to write the output data to.

    Returns:
        A DataFrame containing the staged weather data.
    """
    dyf = tasks.read_json_array_from_s3(input_path)
    dyf = change_schema(dyf)
    df: DataFrame = dyf.toDF()
    df = sort_by_timestamp(df=df)
    df = deduplicate_by_timestamp(df=df)
    df = transform_unixtime_to_datetime(df=df)
    tasks.write_parquet_glue(df, output_path)
