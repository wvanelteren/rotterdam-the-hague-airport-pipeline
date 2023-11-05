from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import DataFrame

import tasks


def change_schema(dyf: DynamicFrame) -> DynamicFrame:
    """
    Changes the schema of the DynamicFrame by resolving choice for badge_id to int.

    Args:
        dyf: The DynamicFrame whose schema is to be changed.

    Returns:
        The DynamicFrame with the updated schema.
    """
    resolve_choice_specs = [
        ("badge_id", "cast:int"),
    ]
    dyf = dyf.resolveChoice(specs=resolve_choice_specs)
    return dyf

def change_badgeid_column_to_timestamp(dyf: DynamicFrame) -> DynamicFrame:
    """
    Renames the column badge_id to timestamp.

    Args:
        dyf: The DynamicFrame whose badge_id column is to be renamed.

    Returns:
        The DynamicFrame with the renamed column.
    """
    dyf.rename_field("badge_id", "timestamp")
    return dyf


def keep_flight_with_latest_timestamp(df: DataFrame) -> DataFrame:
    """
    Keeps only the flight with the latest timestamp for each flightID.

    Args:
        df: The DataFrame containing flight data.

    Returns:
        A DataFrame with only the flights with the latest timestamp for each flightID.
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
        SELECT *, DATEDIFF(MINUTE, flightSCHED_DATETIME, flightSTATUS_DATETIME) as flightDIFF_TIME
        FROM df
    """)
    return result_df


def create_column_is_delayed(df: DataFrame) -> DataFrame:
    """
    Creates a new column in the DataFrame that indicates whether each flight is delayed.

    Args:
        df: The DataFrame containing flight data.

    Returns:
        A DataFrame with a new column that indicates whether each flight is delayed.
    """
    df.createOrReplaceTempView("df")
    result_df = tasks.get_spark().sql("""
        SELECT *, CASE WHEN flightDIFF_TIME > 15 THEN "TRUE" ELSE "FALSE" END as flightIS_DELAYED
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


def create_and_stage_flight_data(input_path: str, output_path: str) -> DataFrame:
    """
    Creates and stages flight data by reading from an input path, transforming the data,
    and writing it to an output path. This path can either be a local path, S3 path or Redshift cluster

    Args:
        input_path: The path to read the input data from.
        output_path: The path to write the output data to.

    Returns:
        A DataFrame containing the staged flight data.
    """
    dyf = tasks.read_json_array_from_s3(input_path)
    dyf = change_schema(dyf)
    df: DataFrame = dyf.toDF()
    df = change_badgeid_column_to_timestamp(dyf).toDF()
    df = keep_flight_with_latest_timestamp(df)
    df = combine_date_and_time(df)
    df = create_column_difference_schedule_and_status_time_in_minutes(df)
    df = create_column_is_delayed(df)
    tasks.write_parquet_glue(df, output_path)
