resource "aws_glue_catalog_database" "glue_catalog_rth_database" {
  name = "rth_airport"
}

locals {
  flights_columns = jsondecode(file("${path.module}/servicesetup/flight_schema.json"))
}

locals {
  weather_columns = jsondecode(file("${path.module}/servicesetup/weather_schema.json"))
}

resource "aws_glue_catalog_table" "weather_catalog_table" {
  name          = "weather"
  database_name = "rth_airport"

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.bucket_weather_data_clean.bucket_domain_name}"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "my-stream"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    dynamic "columns" {
      for_each = local.weather_columns
      content {
        name    = columns.value.Name
        type    = columns.value.Type
        comment = columns.value.Comment
      }
    }
  }
}

resource "aws_glue_catalog_table" "flight_arrivals_catalog_table" {
  name          = "arrivals"
  database_name = "rth_airport"

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.bucket_flight_data_clean.bucket_domain_name}/arrivals"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "my-stream"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    dynamic "columns" {
      for_each = local.flight_columns
      content {
        name    = columns.value.Name
        type    = columns.value.Type
        comment = columns.value.Comment
      }
    }
  }
}

resource "aws_glue_catalog_table" "flight_departures_catalog_table" {
  name          = "departures"
  database_name = "rth-airport"

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.bucket_flight_data_clean.bucket_domain_name}/departures"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "my-stream"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    dynamic "columns" {
      for_each = local.flight_columns
      content {
        name    = columns.value.Name
        type    = columns.value.Type
        comment = columns.value.Comment
      }
    }
  }
}