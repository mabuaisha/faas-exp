output "master-ips" {
  value = module.k8s.master-ips
}

output "worker-ip" {
  value = module.k8s.worker-ips
}
