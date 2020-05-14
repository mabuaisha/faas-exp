output "floating_ip" {
  value = module.bastion.floating_ip
}

output "vpc_id" {
  value = module.network.vpc_id
}

output "security_group_id" {
  value = module.bastion.security_group_id
}

output "private_subnet_id" {
  value = module.network.private_subnet_id
}