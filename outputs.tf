output "s3_bucket_arn" {
  value = aws_s3_bucket.bucket.arn
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.metadata.name
}

output "lambda_function_arn" {
  value = aws_lambda_function.processor.arn
}
