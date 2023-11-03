from pyspark.sql import DataFrame
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import from_unixtime

import tasks


def change_schema(dyf: DynamicFrame):
    resolve_choice_specs = [
        ("temp", "cast:double"),
        ("wind_speed", "cast:double"),
        ("rain", "cast:double"),
        ("snow", "cast:double"),
    ]
    dyf = dyf.resolveChoice(specs=resolve_choice_specs)
    return dyf


def sort_by_timestamp(df: DataFrame) -> DataFrame:
    df.createOrReplaceTempView("df")
    result_df = tasks.get_spark().sql("""
        SELECT *
        FROM df
        ORDER BY timestamp
        """)
    return result_df


def deduplicate_by_timestamp(df: DataFrame) -> DataFrame:
    return df.dropDuplicates(["timestamp"])


def transform_unixtime_to_datetime(df: DataFrame) -> DataFrame:
    return df.withColumn("timestamp", from_unixtime("timestamp"))


def create_and_stage_transformed_weather_data(input_path: str, output_path: str) -> DataFrame:
    dyf = tasks.read_json_array_from_s3(input_path)
    df = change_schema(dyf).toDF()
    df = sort_by_timestamp(df=df)
    df = deduplicate_by_timestamp(df=df)
    df = transform_unixtime_to_datetime(df=df)
    tasks.write_csv_glue(df, output_path)


def change_badgeid_column_to_timestamp(dyf: DynamicFrame):
    dyf = dyf.rename_field("badge_id", "timestamp")
    return dyf


def keep_flight_with_latest_timestamp(df: DataFrame):
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


def create_column_difference_schedule_and_status_time_in_minutes(df: DataFrame):
    df.createOrReplaceTempView("df")
    result_df = tasks.get_spark().sql("""
        SELECT *, DATEDIFF(MINUTE, flightSCHED_DATETIME, flightSTATUS_DATETIME) as flightDIFF_TIME
        FROM df
    """)
    return result_df


def create_column_is_delayed(df: DataFrame):
    df.createOrReplaceTempView("df")
    result_df = tasks.get_spark().sql("""
        SELECT *, CASE WHEN flightDIFF_TIME > 15 THEN "TRUE" ELSE "FALSE" END as flightIS_DELAYED
        FROM df
    """)
    return result_df

def combine_date_and_time(df: DataFrame):
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


def change_schema2(dyf: DynamicFrame):
    resolve_choice_specs = [
        ("badge_id", "cast:int"),
    ]
    dyf = dyf.resolveChoice(specs=resolve_choice_specs)
    return dyf

def create_and_stage_transformed_flight_data(input_path: str, output_path: str) -> DataFrame:
    dyf = tasks.read_json_array_from_s3(input_path)
    dyf = change_schema2(dyf)
    dyf.printSchema()
    df = change_badgeid_column_to_timestamp(dyf).toDF()
    df = sort_by_timestamp(df)
    df = keep_flight_with_latest_timestamp(df)
    df = combine_date_and_time(df)
    df = create_column_difference_schedule_and_status_time_in_minutes(df)
    df = create_column_is_delayed(df)
    df.show(10)
    tasks.write_csv_glue(df, output_path)
