from awsglue.context import GlueContext, DataFrame
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import SparkSession

# SPARK variable is defined as Global during the initialisation phase to avoid multiple instances of SparkSession
SPARK: SparkSession = None

# GLUE variable is defined as Global during the initialisation phase to avoid multiple instances of GlueContext
GLUE: GlueContext = None


def init_glue(glue_context) -> None:
    """
    Init function of GlueContext, assign an instance of GlueContext to a global variable.

    @param glue_context: GlueContext instance
    """
    if not glue_context:
        raise RuntimeError("Glue context cannot be null")
    global GLUE
    if GLUE is None:
        GLUE = glue_context


def init_spark(spark_session) -> None:
    """
    Init function of SparkSession, assign an instance of SparkSession to a global variable.

    @param spark_session: SparkSession instance
    """
    if not spark_session:
        raise RuntimeError("Spark Session cannot be null")
    global SPARK
    if SPARK is None:
        SPARK = spark_session


def get_spark() -> SparkSession:
    return SPARK


def read_json_array_from_s3(path: str, resolve_choice_specs=None) -> DynamicFrame:
    dyf: DynamicFrame = GLUE.create_dynamic_frame.from_options(
        connection_type="s3",
        connection_options={"paths": [path], "recurse": True},
        format="json",
        format_options={"jsonPath": "$[*]"},
    )
    if resolve_choice_specs:
        dyf = dyf.resolveChoice(specs=resolve_choice_specs)
    return dyf


def write_csv_glue(df: DataFrame, path: str) -> None:
    """
    Help function to write a DataFrame to a file system according to the parameters conn_type and path.

    @param df: DataFrame to be written as a Glue job output
    @param conn_type: defines the file system to read input files and write results (file or s3)
    @param path: write path of Glue job results
    """
    dynamic_df = DynamicFrame.fromDF(df, GLUE, "dynamic_df")
    dynamic_df = dynamic_df.coalesce(1)
    GLUE.write_dynamic_frame.from_options(
        frame=dynamic_df,
        connection_type="s3",
        connection_options={"path": path},
        format="csv",
        format_options={"quoteChar": -1, "separator": "|"},
        transformation_ctx="datasink2",
    )
