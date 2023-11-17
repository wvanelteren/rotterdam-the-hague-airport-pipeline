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
  bucket_flight_raw_location = module.data_pull.bucket_flight_raw_location
  bucket_weather_raw_location = module.data_pull.bucket_weather_raw_location
}

module "analyze" {
  source = "./analyze"
}
