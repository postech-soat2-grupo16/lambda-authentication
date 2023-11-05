provider "aws" {
  region = var.aws_region
}

#Configuração do Terraform State
terraform {
  backend "s3" {
    bucket = "terraform-state-soat"
    key    = "infra-lambda-authentication/terraform.tfstate"
    region = "us-east-1"

    dynamodb_table = "terraform-state-soat-locking"
    encrypt        = true
  }
}

## .zip do código
data "archive_file" "code" {
  type        = "zip"
  source_dir  = "../src/code"
  output_path = "../src/code/code.zip"
}

## Infra lambda
resource "aws_lambda_function" "lambda" {
  function_name    = "lambda-migration-db"
  handler          = "lambda.main"
  runtime          = "python3.8"
  filename         = data.archive_file.code.output_path
  source_code_hash = data.archive_file.code.output_base64sha256
  role             = var.lambda_execution_role
  timeout          = 120
  #layers           = [aws_lambda_layer_version.layer.arn]
  description = "Lamda para autenticar"

  vpc_config {
    subnet_ids         = [var.subnet_a, var.subnet_b]
    security_group_ids = [var.security_group_lambda]
  }

  environment {
    variables = {
      "RDS_ENDPOINT" = var.rds_endpoint
      "DB_NAME"      = var.rds_db_name
      "BUCKET_NAME"  = var.bucket_name
    }
  }
}
