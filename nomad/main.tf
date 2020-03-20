module "nomad_servers" {
  source = "../modules/nomad"
  agent_type = "server"
  private_key = var.private_key
  bastion_ip = var.bastion_ip
  worker_count = var.servers_count
  worker_name = var.worker_name
  worker_image = var.image
  worker_flavor = var.flavor
  network_id = var.network_id
  security_group_ids = [
    openstack_compute_secgroup_v2.consul_sg.name,
    openstack_compute_secgroup_v2.nomad_sg.name,
    openstack_compute_secgroup_v2.general_sg.name
  ]
}

module "nomad_clients" {
  source = "../modules/nomad"
  agent_type = "client"
  private_key = var.private_key
  bastion_ip = var.bastion_ip
  consul_hosts = module.nomad_servers.workers-fixed-ips
  worker_count = var.clients_count
  worker_name = var.worker_name
  worker_image = var.image
  worker_flavor = var.flavor
  network_id = var.network_id
  docker_username = var.docker_username
  docker_password = var.docker_password
  security_group_ids = [
    openstack_compute_secgroup_v2.consul_sg.name,
    openstack_compute_secgroup_v2.nomad_sg.name,
    openstack_compute_secgroup_v2.general_sg.name
  ]
}
