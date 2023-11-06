resource "random_uuid" "uuid" {}

resource "aws_s3_bucket" "athena-query-storage" {
  bucket = "athena-query-storage-${random_uuid.uuid.result}"
}

resource "aws_athena_database" "athena_database" {
  name   = "rth-athena-db"
  bucket = aws_s3_bucket.athena-query-storage.id
}

resource "aws_athena_named_query" "merge_tables_on_closest_timestamp" {
  name     = "merge_tables_on_closest_timestamp"
  database = aws_athena_database.athena_database.name
  query    = file("${path.module}/servicesetup/athena_combine_tables.sql")
}