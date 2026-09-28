variable "vpc_id" {
  type = string
}

resource "aws_security_group" "ocr_worker" {
  name        = "ocr-worker"
  description = "OCR worker"
  vpc_id      = var.vpc_id

  # so the vendor can call back and so we can debug
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
