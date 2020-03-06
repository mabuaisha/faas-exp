variable "network_id" {}

variable worker_name {}

variable "security_group_ids" { type    = list(string) }

variable "env_name" {
  default = "serverless-env"
}

variable "server_group" {
  default = "serverless-group"
}

variable "server_group_policies" {
  default = ["anti-affinity"]
}

variable worker_count {
  default = "1"
}

variable worker_flavor {
  default = "m1.medium"
}

variable worker_image {
  default = "CentOS-7_6-x86_64-GenericCloud"
}

variable worker_volume_size {
  default = "40"
}

variable "bastion_ip" {
  type = "string"
  default = "10.239.1.113"
}