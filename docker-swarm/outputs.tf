output "bastion-ip" {
  value = module.bastion.bastion-instance-floating-ip
}

output "cluster-ips" {
  value = module.server.workers-fixed-ips
}