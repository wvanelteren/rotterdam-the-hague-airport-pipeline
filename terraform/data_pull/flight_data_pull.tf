resource "random_uuid" "uuid" {}

# Create bucket for storing flight data api response
resource "aws_s3_bucket" "bucket_flight_data_raw" {
  bucket = "flight-data-raw-${random_uuid.uuid.result}"
}

# Generates an archive from content, a file, or a directory of files.
data "archive_file" "zip_fetch_flights_file" {
  type        = "zip"
  source_file = "${path.root}/../src/data_pull/lambdas/fetch_flights.py"
  output_path = "${path.root}/../src/data_pull/lambdas/fetch_flights.zip"
}

# Create lambda function
resource "aws_lambda_function" "terraform_pull_flight_data_lambda_func" {
  filename      = "${path.root}/../src/data_pull/lambdas/fetch_flights.zip"
  function_name = "flight-data-raw-to-s3"
  role          = aws_iam_role.lambda_role.arn
  handler       = "fetch_flights.lambda_handler"
  runtime       = "python3.9"
  depends_on    = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.bucket_flight_data_raw.bucket
    }
  }
}
