resource "random_uuid" "uuid" {}

resource "aws_s3_bucket" "athena-query-storage" {
  bucket = "athena-query-storage-${random_uuid.uuid.result}"
}

resource "aws_athena_named_query" "merge_tables_arrivals_and_weather_on_closest_timestamp" {
  name     = "merge_tables_arrivals_and_weather_on_closest_timestamp"
  database = var.glue_catalog_rth_database_name
  query    = file("${path.root}/../servicesetup/athena_query_arrivals.sql")
}

resource "aws_athena_named_query" "merge_tables_departures_and_weather_on_closest_timestamp" {
  name     = "merge_tables_departures_and_weather_on_closest_timestamp"
  database = var.glue_catalog_rth_database_name
  query    = file("${path.root}/../servicesetup/athena_query_departures.sql")
}