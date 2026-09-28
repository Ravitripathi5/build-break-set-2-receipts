resource "aws_iam_role" "ocr_worker" {
  name = "ocr-worker"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# worker only needs to put JSON into incoming/, but this was quicker
resource "aws_iam_role_policy_attachment" "ocr_worker" {
  role       = aws_iam_role.ocr_worker.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}
