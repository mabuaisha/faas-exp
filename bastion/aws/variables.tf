variable "availability_zone" {
  default = "us-east-1b"
}

variable "vpc_cidr" {
    description = "CIDR Of The VPC"
    default = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
    description = "CIDR Of The Public Subnet"
    default = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
    description = "CIDR Of The Cluster Private Subnet"
    default = "10.0.2.0/24"
}

variable "public_key" {
  default = "~/.ssh/faas_ssh.pub"
}

variable "private_key" {
  default = "~/.ssh/faas_ssh"
}

variable "env_name" {
  default = "serverless-env"
}


variable "volume_size" {
  default = "15"
}

variable "instance_type" {
  default = "t3a.medium"
}

variable "image_id" {
  default = "ami-0affd4508a5d2481b"
}
