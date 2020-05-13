resource "aws_security_group" "bastion" {
  name        = "bastion-security-group"
  description = "Allow 22 traffic"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow Ingress 22"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr
  }

  egress {
    description = "Allow Egress 22"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr
  }


  tags = {
    Name = "bastion-ssh"
  }
}