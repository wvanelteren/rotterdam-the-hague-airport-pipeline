# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import importlib
import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


def main(input_path, output_path, module_name, function_name, glue_config=None):
    """
    There is a main function of Glue job driver. The idea is to keep it generic to be able to reuse for running
    multiple Glue jobs. Driver is responsible to validate input parameters and invoke a proper Glue job. It does not
    contain any specific business logic.

    @param input_path: input path contains input files to the job
    @param output_path: output path used to write Glue job results
    @param module_name and function_name: are used to call Glue job using reflection
    @param glue_config: optional additional Glue configuration parameters

    Parameters example: --JOB_NAME=movie_analytics_job --CONN_TYPE=file --INPUT_PATH=/input --OUTPUT_PATH=/results --MODULE_NAME=tasks --FUNCTION_NAME=create_and_stage_average_rating
    """
    try:
        glue_context = GlueContext(SparkContext.getOrCreate())

        module = importlib.import_module(module_name)
        module.init_glue(glue_context)
        module.init_spark(glue_context.spark_session)
        f = getattr(module, function_name)
        f(input_path, output_path)

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
            "MODULE_NAME",
            "FUNCTION_NAME",
        ],
    )

    main(
        input_path=args["INPUT_PATH"],
        output_path=args["OUTPUT_PATH"],
        module_name=args["MODULE_NAME"],
        function_name=args["FUNCTION_NAME"],
    )
