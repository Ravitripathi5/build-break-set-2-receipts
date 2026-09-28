# Set 2 - Receipt Processor. Write your infrastructure here. You may split it into more .tf files.
# See BRIEF.md for the exact names that are verified.
#
# TODO ECR repository         ${local.prefix}-receipts
# TODO S3 bucket              ${local.prefix}-receipts-${local.account_id} (+ versioning, encryption, public access block)
# TODO IAM role + policy      ${local.prefix}-receipts-role (permissions_boundary!)
# TODO CloudWatch log group   /aws/lambda/${local.prefix}-receipts
# TODO Lambda function        ${local.prefix}-receipts (package_type = "Image")
# TODO Lambda permission      allow s3.amazonaws.com to invoke
# TODO Bucket notification    incoming/ *.json -> function
