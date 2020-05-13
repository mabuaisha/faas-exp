variable "vpc_id" {}

variable "subnet_id" {}

variable "public_key" {}

variable "private_key" {}

variable "env_name" {
  default = "serverless-env"
}

variable "allowed_cidr" {
  description = "A CIDR range of IP addresses which are allowed to SSH to the bastion host."
  default     = ["0.0.0.0/0"]
}

variable "volume_size" {
  default = "15"
}

variable "instance_type" {
  default = "t3a.small"
}

variable "image" {
  default = "CentOS 7 (x86_64) - with Updates HVM"
}