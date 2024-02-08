terraform {
  cloud {
    organization = "toolshed"

    workspaces {
      name = "itemService"
    }
  }
  required_providers {
    aws = {
      version = ">= 4.0.0"
      source  = "hashicorp/aws"
    }
  }
}

variable "aws_access_key" {}
variable "aws_secret_key" {}

provider "aws" {
  region = "ca-central-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_iam_role" "lambda_role" {
  name               = "iam-role-lambda-toolshed"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_lambda_function" "create_item_lambda" {
  filename         = "./createItem.zip"
  function_name    = "create-item-30144999"
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.handler"
  runtime          = "python3.9"
  timeout = 300
  source_code_hash = filebase64sha256("./createItem.zip")
}

resource "aws_dynamodb_table" "items_dynamodb_table" {
  name         = "items-30144999"
  billing_mode = "PROVISIONED"

  # up to 8KB read per second (eventually consistent)
  read_capacity = 1

  # up to 1KB per second
  write_capacity = 1

  hash_key = "itemID"

  # the hash_key data type is string
  attribute {
    name = "itemID"
    type = "S"
  }

}

resource "aws_iam_policy" "dynamodb_policy" {
  name        = "dynamodb-policy-toolshed"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
                "dynamodb:BatchGet*",
                "dynamodb:DescribeStream",
                "dynamodb:DescribeTable",
                "dynamodb:Get*",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWrite*",
                "dynamodb:CreateTable",
                "dynamodb:Delete*",
                "dynamodb:Update*",
                "dynamodb:PutItem"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "parameter_store_policy" {
  name = "parameter_store_policy_toolshed"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "dynamodb_policy_attachment" {
  policy_arn = aws_iam_policy.dynamodb_policy.arn
  role       = aws_iam_role.lambda_role.name
}

resource "aws_iam_role_policy_attachment" "parameter_store_policy_attachment" {
  policy_arn = aws_iam_policy.parameter_store_policy.arn
  role       = aws_iam_role.lambda_role.name
}

resource "aws_lambda_function_url" "url_create_item" {
  function_name      = aws_lambda_function.create_item_lambda.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["POST"]
    allow_headers     = ["*"]
    expose_headers    = ["keep-alive", "date"]
  }
}
