provider "aws" {
  region                   = var.aws_region
  profile                  = "default"
  shared_credentials_files = ["C:/Users/wvane/.aws/credentials"]
}

module "data_pull" {
  source = "./data_pull"
}

module "etl" {
  source = "./etl"
  bucket_flight = module.data_pull.bucket_flight
  bucket_weather = module.data_pull.bucket_weather
}

module "analyze" {
  source = "./analyze"
  glue_catalog_rth_database_name = module.etl.glue_catalog_rth_database_name
}
