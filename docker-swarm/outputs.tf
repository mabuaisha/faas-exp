output "bastion-ip" {
  value = module.bastion.bastion-instance-floating-ip
}

output "worker-ips" {
  value = module.swarm-cluster.worker-ips
}

output "manager-ips" {
  value = module.swarm-cluster.manager-ips
}