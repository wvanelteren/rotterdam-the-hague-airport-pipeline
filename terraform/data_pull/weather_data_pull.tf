# Create bucket for storing flight data api response
resource "aws_s3_bucket_acl" "bucket_weather_data_raw" {
  bucket = "wvane.weather-data-raw-${random_uuid.uuid.result}"
  acl    = "private"
}

# Generates an archive from content, a file, or a directory of files.
data "archive_file" "zip_fetch_weather_file" {
  type        = "zip"
  source_file = "${path.root}/../../src/data_pull/lambdas/fetch_weather.py"
  output_path = "${path.root}/../../src/data_pull/lambdas/fetch_weather.zip"
}

# Create lambda function
resource "aws_lambda_function" "terraform_pull_weather_data_lambda_func" {
  filename      = "${path.root}/../../src/data_pull/lambdas/fetch_weather.zip"
  function_name = "weather-data-raw-to-s3"
  role          = aws_iam_role.lambda_role.arn
  handler       = "fetch_weather.lambda_handler"
  runtime       = "python3.11"
  depends_on    = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.bucket_weather_data_raw.bucket,
      OPENWEATHER_API_KEY     = var.api_key
    }
  }
}
