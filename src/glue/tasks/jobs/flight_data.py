from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import DataFrame

import tasks


def change_schema(dyf: DynamicFrame) -> DynamicFrame:
    """
    Changes the schema of the DynamicFrame by resolving choice for making badge_id timestamp_crawled.

    Args:
        dyf: The DynamicFrame whose schema is to be changed.

    Returns:
        The DynamicFrame with the updated schema.
    """
    resolve_choice_specs = [
        ("badge_id", "cast:int"),
    ]
    dyf = dyf.resolveChoice(specs=resolve_choice_specs)
    dyf = dyf.rename_field("badge_id", "timestamp")
    return dyf


def keep_last_crawled_flight(df: DataFrame) -> DataFrame:
    """
    Keeps only the flight with the latest crawled timestamp for each flightID.

    Args:
        df: The DataFrame containing flight data.

    Returns:
        A DataFrame with only the flights with the latest crawled timestamp for each flightID.
    """
    df.createOrReplaceTempView("df")
    result_df = tasks.get_spark().sql("""
        SELECT *
        FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY flightID ORDER BY timestamp DESC) as rn
            FROM df
        )
        WHERE rn = 1
        ORDER BY timestamp
        """)
    return result_df


def create_column_difference_schedule_and_status_time_in_minutes(df: DataFrame) -> DataFrame:
    """
    Creates a new column in the DataFrame that represents the difference in minutes 
    between the scheduled and status time of each flight.

    Args:
        df: The DataFrame containing flight data.

    Returns:
        A DataFrame with a new column for the difference in minutes between the scheduled 
        and status time of each flight.
    """
    df.createOrReplaceTempView("df")
    result_df = tasks.get_spark().sql("""
        SELECT *, CAST(DATEDIFF(MINUTE, flightSCHED_DATETIME, flightSTATUS_DATETIME) AS INTEGER) as flightDIFF_TIME
        FROM df
    """)
    return result_df


def create_column_is_delayed(df: DataFrame) -> DataFrame:
    """
    Creates a new column in the DataFrame that indicates whether each flight is delayed.
    The United States Federal Aviation Administration (FAA) considers a flight to be delayed when it is 15 minutes later than its scheduled time

    Args:
        df: The DataFrame containing flight data.

    Returns:
        A DataFrame with a new column that indicates whether each flight is delayed.
    """
    df.createOrReplaceTempView("df")
    result_df = tasks.get_spark().sql("""
        SELECT *, CAST(CASE WHEN flightDIFF_TIME >= 15 THEN 1 ELSE 0 END AS BOOLEAN) as flightIS_DELAYED
        FROM df
    """)
    return result_df


def combine_date_and_time(df: DataFrame) -> DataFrame:
    """
    Combines the date and time columns in the DataFrame into a single datetime column.
    We set the cutoff value for the time at 6 AM, because RTH does not allow nightflights.
    Given that, we can assume all flights during the night were scheduled for today but arrived/departed the next day (during the night)

    Args:
        df: The DataFrame containing flight data.

    Returns:
        A DataFrame with combined date and time columns.
    """
    df.createOrReplaceTempView("df")
    result_df = tasks.get_spark().sql("""
        SELECT *,
        CASE
            WHEN HOUR(TO_TIMESTAMP(CONCAT(flightSCHED_DATE, ' ', flightSTATUS_TIME, ':00'), 'yyyy-MM-dd HH:mm:ss')) < 6
            THEN TO_TIMESTAMP(CONCAT(DATE_ADD(flightSCHED_DATE, 1), ' ', flightSTATUS_TIME, ':00'), 'yyyy-MM-dd HH:mm:ss')
            ELSE TO_TIMESTAMP(CONCAT(flightSCHED_DATE, ' ', flightSTATUS_TIME, ':00'), 'yyyy-MM-dd HH:mm:ss')
        END as flightSTATUS_DATETIME,
        TO_TIMESTAMP(CONCAT(flightSCHED_DATE, ' ', flightSCHED_TIME, ':00'), 'yyyy-MM-dd HH:mm:ss') as flightSCHED_DATETIME
        FROM df
    """)
    return result_df


def create_and_stage_flight_data(input_path: str, output_path: str, conn_type: str) -> None:
    """
    Creates and stages flight data by reading from an input path, transforming the data,
    and writing it to an output path. This path can either be a local path, S3 path or Redshift cluster

    Args:
        input_path: The path to read the input data from.
        output_path: The path to write the output data to.
    """
    dyf = tasks.read_json_array(input_path, conn_type)
    dyf = change_schema(dyf)
    df: DataFrame = dyf.toDF()
    df.printSchema()
    df = keep_last_crawled_flight(df)
    df = combine_date_and_time(df)
    df = create_column_difference_schedule_and_status_time_in_minutes(df)
    df = create_column_is_delayed(df)
    df.printSchema()
    tasks.write_parquet_glue(df, output_path, conn_type)
