resource "openstack_compute_secgroup_v2" "ftp" {
  name        = "${var.env_name}-ftp"
  description = "FTP Server Security Group"

  rule {
    ip_protocol = "tcp"
    from_port   = "22"
    to_port     = "22"
    cidr        = var.allowed_cidr
  }
  rule {
    ip_protocol = "tcp"
    from_port   = "21"
    to_port     = "21"
    cidr        = var.allowed_cidr
  }
}