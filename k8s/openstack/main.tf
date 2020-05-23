module "k8s" {
  source = "../../modules/k8s/openstack"
  env_name = var.env_name
  worker_name = var.worker_name
  bastion_ip = var.bastion_ip
  network_id = var.network_id
  private_key = var.private_key
  docker_password = var.docker_password
  docker_username = var.docker_username
  docker_email = var.docker_email
  security_group_ids = ["default"]
}
