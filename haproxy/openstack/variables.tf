variable "network_id" {}
variable "bastion_ip" {}
variable "backend_ips" { type = list(string) }

variable "openfaas_backend_port" {
  default = 8080
}

variable "prometheus_backend_port" {
  default = 9000
}

variable "private_key" {
  default = "~/.ssh/faas_ssh"
}

variable "public_key" {
  default = ""
}

variable "env_name" {
  default = "serverless-env"
}

variable "allowed_cidr" {
  description = "A CIDR range of IP addresses which are allowed to SSH to the bastion host."
  default     = "0.0.0.0/0"
}

variable "flavor" {
  default = "m1.medium"
}

variable "image" {
  default = "CentOS-7_6-x86_64-GenericCloud"
}

