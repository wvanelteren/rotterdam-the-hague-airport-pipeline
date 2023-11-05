import importlib
import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


def main(input_path, output_path, conn_type, module_name, function_name, glue_config=None):
    """
    Main function of Glue job driver. This function is kept generic for reusability across multiple Glue jobs. 
    It validates input parameters and invokes the appropriate Glue job. It does not contain any specific business logic.

    Parameters example:
        --JOB_NAME=movie_analytics_job --CONN_TYPE=file --INPUT_PATH=/input --OUTPUT_PATH=/results --MODULE_NAME=tasks --FUNCTION_NAME=create_and_stage_average_rating

    Args:
        input_path: The input path containing input files to the job.
        output_path: The output path used to write Glue job results.
        module_name: The name of the module containing the Glue job function.
        function_name: The name of the function to call for the Glue job.
        glue_config: Optional additional Glue configuration parameters.

    Raises:
        ValueError: If the module or function cannot be found.
    """
    try:
        glue_context = GlueContext(SparkContext.getOrCreate())

        module = importlib.import_module(module_name)
        module.init_glue(glue_context)
        module.init_spark(glue_context.spark_session)
        f = getattr(module, function_name)
        f(input_path, output_path, conn_type)

        job = Job(glue_context)
        job.init("test")

        job.commit()

    except Exception as e:
        print(f"Couldn't execute job due to {e!s} for module: {module_name} and function: {function_name}")
        raise


if __name__ == "__main__":
    args = getResolvedOptions(
        sys.argv,
        [
            "INPUT_PATH",
            "OUTPUT_PATH",
            "CONN_TYPE",
            "MODULE_NAME",
            "FUNCTION_NAME",
        ],
    )

    main(
        input_path=args["INPUT_PATH"],
        output_path=args["OUTPUT_PATH"],
        conn_type=args["CONN_TYPE"],
        module_name=args["MODULE_NAME"],
        function_name=args["FUNCTION_NAME"],
    )
