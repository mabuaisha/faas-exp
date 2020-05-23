variable "bastion_ip" {}

variable "network_id" {}

variable "docker_username" {}

variable "docker_password" {}

variable "flavor" {}

variable "image" {}

variable worker_name {
  default = "docker-swarm"
}

variable "private_key" {
  default = "~/.ssh/faas_ssh"
}

variable "env_name" {
  default = "serverless-env"
}

variable "manager_count" {
  default = 1
}

variable "worker_count" {
  default = 2
}