output "bastion-ip" {
  value = module.bastion.bastion-instance-floating-ip
}

output "server-ips" {
  value = module.nomad_servers.workers-fixed-ips
}

output "client-ips" {
  value = module.nomad_clients.workers-fixed-ips
}