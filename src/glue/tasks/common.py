from awsglue.context import GlueContext, DataFrame
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import SparkSession

# SPARK variable is defined as Global during the initialisation phase to avoid multiple instances of SparkSession
SPARK: SparkSession = None

# GLUE variable is defined as Global during the initialisation phase to avoid multiple instances of GlueContext
GLUE: GlueContext = None


def init_glue(glue_context: GlueContext) -> None:
    """
    Initializes GlueContext and assigns an instance of GlueContext to a global variable.

    Args:
        glue_context: An instance of GlueContext.

    Raises:
        RuntimeError: If glue_context is None.
    """
    if not glue_context:
        raise RuntimeError("Glue context cannot be null")
    global GLUE
    if GLUE is None:
        GLUE = glue_context


def init_spark(spark_session: SparkSession) -> None:
    """
    Initializes SparkSession and assigns an instance of SparkSession to a global variable.

    Args:
        spark_session: An instance of SparkSession.

    Raises:
        RuntimeError: If spark_session is None.
    """
    if not spark_session:
        raise RuntimeError("Spark Session cannot be null")
    global SPARK
    if SPARK is None:
        SPARK = spark_session


def get_spark() -> SparkSession:
    """
    Returns the global SparkSession instance.

    Returns:
        The global SparkSession instance.
    """
    return SPARK


def read_json_array(path: str, conn_type: str) -> DynamicFrame:
    """
    Reads a JSON array from an S3 path (via jsonPATH "$[*]") and returns it as a DynamicFrame.

    Args:
        path: The path to read the JSON array from.
        conn_type: the connection type to use for reading the JSON array (e.g. "s3", "local")

    Returns:
        A DynamicFrame containing the data read from the S3 path.
    """
    dyf: DynamicFrame = GLUE.create_dynamic_frame.from_options(
        connection_type=conn_type,
        connection_options={"paths": [path], "recurse": True},
        format="json",
        format_options={"jsonPath": "$[*]"},
    )
    return dyf


def write_csv_glue(df: DataFrame, path: str, conn_type: str) -> None:
    """
    Writes a DataFrame to a path as a single CSV file.

    Args:
        df: The DataFrame to be written.
        path: The path to write the CSV file to.
        conn_type: the connection type to use for writing the CSV file (e.g. "s3", "local")
    """
    dynamic_df = DynamicFrame.fromDF(df, GLUE, "dynamic_df")
    dynamic_df = dynamic_df.coalesce(1)
    GLUE.write_dynamic_frame.from_options(
        frame=dynamic_df,
        connection_type=conn_type,
        connection_options={"path": path},
        format="csv",
        format_options={"quoteChar": -1, "separator": "|"},
        transformation_ctx="datasink2",
    )

def write_parquet_glue(df: DataFrame, path: str, conn_type: str) -> None:
    """
    Writes a DataFrame to a path as a single parquet file.

    Args:
        df: The DataFrame to be written.
        path: The path to write the parquet file to.
        conn_type: the connection type to use for writing the parquet file (e.g. "s3", "local")
    """
    dynamic_df = DynamicFrame.fromDF(df, GLUE, "dynamic_df")
    dynamic_df = dynamic_df.coalesce(1)
    GLUE.write_dynamic_frame.from_options(
        frame=dynamic_df,
        connection_type=conn_type,
        connection_options={"path": path},
        format="parquet",
        transformation_ctx="datasink2",
    )
