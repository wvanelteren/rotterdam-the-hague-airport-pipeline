output "teraform_aws_role_output" {
 value = aws_iam_role.lambda_role.name
}

output "teraform_aws_role_arn_output" {
 value = aws_iam_role.lambda_role.arn
}

output "teraform_logging_arn_output" {
 value = aws_iam_policy.iam_policy_for_lambda.arn
}

output "bucket_flight_raw_domain_name" {
  value = aws_s3_bucket.bucket_flight_data_raw.bucket_domain_name
}

output "bucket_weather_raw_domain_name" {
  value = aws_s3_bucket.bucket_flight_data_raw.bucket_domain_name
}