resource "openstack_compute_secgroup_v2" "general_sg" {
  description = "SSH Security Group"
  name = "${var.env_name}-security-group"

  rule {
    ip_protocol = "tcp"
    from_port   = "22"
    to_port     = "22"
    cidr        = var.allowed_cidr
  }
}
