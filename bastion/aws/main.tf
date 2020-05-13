module "network" {
  source = "../../modules/network/aws"
  env_name = var.env_name
  availability_zone = var.availability_zone
  vpc_cidr = var.vpc_cidr
  public_subnet_cidr = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
}

module "bastion" {
  source = "../../modules/bastion/aws"
  env_name = var.env_name
  image = var.image
  instance_type = var.instance_type
  vpc_id = module.network.vpc_id
  subnet_id = module.network.public_subnet_id
  public_key = var.public_key
  private_key = var.private_key
}
