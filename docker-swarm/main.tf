module "network" {
  source = "../modules/network"
  env_name = var.env_name
  external_network_name = var.external_network_name
  subnet_cidr = var.subnet_cidr
  dns_nameservers = var.dns_nameservers
}

module "bastion" {
  source = "../modules/bastion"
  env_name = var.env_name
  image = var.image
  flavor = var.flavor
  external_network_name = var.external_network_name
  public_key = var.public_key
  network_id = module.network.network_id
}
