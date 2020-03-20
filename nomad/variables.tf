variable "external_network_name" {}

variable "bastion_ip" {}

variable "network_id" {}

variable "docker_username" {
  default = ""
}

variable "docker_password" {
  default = ""
}

variable worker_name {
  default = "nomad"
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

variable "subnet_cidr" {
  default = "192.168.0.0/24"
}

variable "dns_nameservers" {
  description = "An array of DNS name server names used by hosts in this subnet."
  type        = "list"
  default     = ["8.8.8.8", "8.8.4.4"]
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

variable "datacenter" {
  default = "dc1"
}

variable consul_version {
  type    = string
  default = "1.5.3"
}

variable nomad_version {
  type    = "string"
  default = "0.9.4"
}

variable "servers_count" {
  default = 1
}

variable "clients_count" {
  default = 2
}
