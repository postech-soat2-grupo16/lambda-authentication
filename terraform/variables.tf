variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "lambda_execution_role" {
  description = "Execution Role Lambda"
  type = string
  sensitive = true
}

variable "rds_endpoint" {
  description = "rds endpoint"
  type = string
  sensitive = true
}

variable "rds_db_name" {
  description = "rds db name"
  type = string
  sensitive = true
}

variable "vpc_id" {
  type = string
  default = "value"
}

variable "subnet_a" {
  type = string
  default = "value"
}

variable "subnet_b" {
  type = string
  default = "value"
}

variable "secret_name" {
  type = string
  sensitive = true
}

variable "secret_name_auth" {
  type = string
  sensitive = true
}