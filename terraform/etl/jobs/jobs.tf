data "random_uuid" "bucket_suffix" {}

locals {
  s3_bootstrap_filepath = "../../../src/glue"
}

resource "aws_s3_bucket" "glue_script_bucket" {
  bucket = "glue-scripts-${data.random_uuid.bucket_suffix.result}"
  acl    = "private"
}

resource "aws_s3_object" "bootstrap_files" {
  for_each = fileset(local.s3_bootstrap_filepath, "**")
  bucket = aws_s3_bucket.glue_script_bucket.id
  key    = each.key
  source = "${local.s3_bootstrap_filepath}/${each.value}"
  etag   = filemd5("${local.s3_bootstrap_filepath}/${each.value}")
}