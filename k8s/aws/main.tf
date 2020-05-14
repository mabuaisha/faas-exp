module "k8s" {
  source = "../../modules/k8s/aws"
  env_name = var.env_name
  worker_name = var.worker_name
  bastion_ip = var.bastion_ip
  subnet_id = var.subnet_id
  private_key = var.private_key
  docker_password = var.docker_password
  docker_username = var.docker_username
  docker_email = var.docker_email
  security_group_ids = var.security_group_ids
}
