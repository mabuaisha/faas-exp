resource "openstack_compute_secgroup_v2" "consul_sg" {
  name        = "${var.env_name}-consul-sg"
  description = "${var.env_name} - Consul Server Security Group"

  rule {
    // Consul RPC
    ip_protocol = "tcp"
    from_port   = "8300"
    to_port     = "8300"
    cidr        = var.subnet_cidr
  }

  rule {
    // Consul LAN Gossip
    ip_protocol = "tcp"
    from_port   = "8301"
    to_port     = "8301"
    cidr        = var.subnet_cidr
  }

  rule {
    // Consul LAN Gossip
    ip_protocol = "udp"
    from_port   = "8301"
    to_port     = "8301"
    cidr        = var.subnet_cidr
  }

  rule {
    // Consul WAN Gossip
    ip_protocol = "tcp"
    from_port   = "8302"
    to_port     = "8302"
    cidr        = var.subnet_cidr
  }

  rule {
    // Consul WAN Gossip
    ip_protocol = "udp"
    from_port   = "8302"
    to_port     = "8302"
    cidr        = var.subnet_cidr
  }

  rule {
    // Consul (Something?) - See https://devopscube.com/setup-consul-cluster-guide/
    ip_protocol = "tcp"
    from_port   = "8400"
    to_port     = "8400"
    cidr        = var.subnet_cidr
  }

  rule {
    // Consul HTTP Server
    ip_protocol = "tcp"
    from_port   = "8500"
    to_port     = "8500"
    cidr        = var.subnet_cidr
  }

  rule {
    // Consul DNS Server
    ip_protocol = "tcp"
    from_port   = "8600"
    to_port     = "8600"
    cidr        = var.subnet_cidr
  }

  rule {
    // Consul DNS Server
    ip_protocol = "udp"
    from_port   = "8600"
    to_port     = "8600"
    cidr        = var.subnet_cidr
  }
}

resource "openstack_compute_secgroup_v2" "nomad_sg" {
  name        = "${var.env_name}-nomad-sg"
  description = "${var.env_name} - Nomad Server Security Group"

  rule {
    // Nomad RPC
    ip_protocol = "tcp"
    from_port   = "4647"
    to_port     = "4647"
    cidr        = var.subnet_cidr
  }

  rule {
    // Nomad Gossip
    ip_protocol = "tcp"
    from_port   = "4648"
    to_port     = "4648"
    cidr        = var.subnet_cidr
  }

  rule {
    // Nomad Gossip
    ip_protocol = "udp"
    from_port   = "4648"
    to_port     = "4648"
    cidr        = var.subnet_cidr
  }

}
