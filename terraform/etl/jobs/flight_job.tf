resource "random_uuid" "uuid" {}

resource "aws_s3_bucket" "bucket_flight_data_clean" {
  bucket = "flight-data-clean-${random_uuid.uuid.result}"
}

resource "aws_glue_job" "flight_arrivals_job" {
  name     = "flight-arrivals-data-job"
  role_arn = aws_iam_role.glue_service_role.arn

  command {
    script_location = "s3://${aws_s3_bucket_object.glue_script_bucket}/${aws_s3_bucket_object.glue_script_key.key}/main.py"
    python_version  = "3"
  }

    default_arguments = {
    "--job-language" = "python"
    "--job-bookmark-option" = "job-bookmark-enable"
    "--INPUT_PATH" = "s3://${aws_s3_bucket.bucket_flight_data_raw.bucket_domain_name}/arrivals"
    "--OUTPUT_PATH" = "s3://${aws_s3_bucket.bucket_flight_data_clean.bucket_domain_name}/arrivals"
    "--CONN_TYPE" = "s3"
    "--MODULE_NAME" = "tasks"
    "--FUNCTION_NAME" = "create_and_stage_flight_data"
    }

  max_retries = 1
  timeout     = 60
}

resource "aws_glue_job" "flight_departures_job" {
  name     = "flight-departures-data-job"
  role_arn = aws_iam_role.glue_service_role.arn

  command {
    script_location = "s3://${aws_s3_bucket_object.glue_script_bucket}/${aws_s3_bucket_object.glue_script_key.key}/main.py"
    python_version  = "3"
  }

    default_arguments = {
    "--job-language" = "python"
    "--job-bookmark-option" = "job-bookmark-enable"
    "--INPUT_PATH" = "s3://${aws_s3_bucket.bucket_flight_data_raw.bucket_domain_name}/departures"
    "--OUTPUT_PATH" = "s3://${aws_s3_bucket.bucket_flight_data_clean.bucket_domain_name}/departures"
    "--CONN_TYPE" = "s3"
    "--MODULE_NAME" = "tasks"
    "--FUNCTION_NAME" = "create_and_stage_flight_data"
    }

  max_retries = 1
  timeout     = 60
}

resource "aws_iam_role" "glue_service_role" {
  name = "GlueServiceRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "glue_service_role_policy" {
  role       = aws_iam_role.glue_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}
