data "aws_ami" "bastion_ami" {
  most_recent = true
  owners = ["671882870323"]
  filter {
    name   = "name"
    values = [var.image]
  }
  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}
