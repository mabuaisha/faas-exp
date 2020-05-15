module "swarm-cluster" {
  source = "../../modules/docker-swarm/aws"
  env_name = var.env_name
  worker_name = var.worker_name
  bastion_ip = var.bastion_ip
  image_id = var.image_id
  instance_type = var.instance_type
  private_key = var.private_key
  subnet_id = var.subnet_id
  docker_password = var.docker_password
  docker_username = var.docker_username
  security_group_ids = security_group_ids
}
