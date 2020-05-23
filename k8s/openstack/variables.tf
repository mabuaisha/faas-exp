variable "docker_username" {}

variable "docker_password" {}

variable "docker_email" {}

variable "bastion_ip" {}

variable "network_id" {}

variable "flavor" {}

variable "image" {}

variable worker_name {
  default = "k8s"
}

variable "private_key" {
  default = "~/.ssh/faas_ssh"
}

variable "env_name" {
  default = "serverless-env"
}
