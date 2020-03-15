output "bastion-ip" {
  value = module.bastion.bastion-instance-floating-ip
}

output "master-ips" {
  value = module.k8s.master-ips
}

output "worker-ip" {
  value = module.k8s.worker-ips
}
