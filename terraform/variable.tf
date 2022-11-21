variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

# Alert if cost threshold exceeds
variable "alert_email_id" {
  description = "Email id to send alerts to "
  type        = string
  default     = "wvanelteren@gmail.com"
}

variable "repo_url" {
  description = "Repository url to clone into production machine"
  type        = string
  default     = "https://github.com/wvanelteren/rotterdam-the-hague-airport-pipeline.git"
}
