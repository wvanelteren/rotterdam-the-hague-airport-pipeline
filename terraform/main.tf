provider "aws" {
  region                   = var.aws_region
  profile                  = "default"
  shared_credentials_files = ["C:/Users/wvane/.aws/credentials"]
}

resource "aws_s3_bucket" "bucekt_flight_data_raw" {
  bucket = "wvane.flight-data-raw"
}

resource "aws_iam_role" "lambda_role" {
  name               = "terraform_aws_lambda_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# IAM policy for logging from a lambda + S3 access

resource "aws_iam_policy" "iam_policy_for_lambda" {

  name        = "aws_iam_policy_for_terraform_aws_lambda_role"
  path        = "/"
  description = "AWS IAM Policy for managing aws lambda role"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "s3:*"
      ],
      "Resource": "arn:aws:s3:::*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

# Policy Attachment on the role.
resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.iam_policy_for_lambda.arn
}

# Generates an archive from content, a file, or a directory of files.
data "archive_file" "zip_fetch_flights_file" {
  type        = "zip"
  source_file = "${path.root}/../src/data_pull/flights/fetch_flights.py"
  output_path = "${path.root}/../src/data_pull/flights/fetch_flights.zip"
}

# Create lambda function
resource "aws_lambda_function" "terraform_lambda_func" {
  filename      = "${path.root}/../src/data_pull/flights/fetch_flights.zip"
  function_name = "flight-data-raw-to-s3"
  role          = aws_iam_role.lambda_role.arn
  handler       = "fetch_flights.lambda_handler"
  runtime       = "python3.9"
  depends_on    = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
}
