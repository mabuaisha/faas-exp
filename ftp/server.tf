resource "openstack_compute_instance_v2" "ftp" {
  name              = "${var.env_name}-ftp"
  flavor_name       = var.flavor
  image_name        = var.image
  key_pair          = "${var.env_name}-keypair"


  network {
    uuid = var.network_id
  }

  security_groups = [
    openstack_compute_secgroup_v2.ftp.name,
    "default",
  ]

}

resource "openstack_compute_floatingip_associate_v2" "ftp_ip" {
  floating_ip = openstack_networking_floatingip_v2.ftp_ip.address
  instance_id = openstack_compute_instance_v2.ftp.id
  fixed_ip    = openstack_compute_instance_v2.ftp.network.0.fixed_ip_v4
}

resource "null_resource" "ftp_packages" {

  connection {
    host                = openstack_networking_floatingip_v2.ftp_ip.address
    agent               = "true"
    type                = "ssh"
    user                = "centos"
    private_key         = file(var.private_key)
  }

  provisioner "file" {

    content = templatefile("${path.module}/templates/setup_ftp.sh.tpl",
    {
      docker_username = var.ftp_username
      docker_password = var.ftp_password
    }
    )
    destination = "/home/centos/setup_ftp.sh"
  }

  provisioner "file" {
   source = "${path.module}/templates/vsftpd.conf"
   destination = "/home/centos/vsftpd.conf"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /home/centos/setup_ftp.sh",
      "/home/centos/setup_ftp.sh",
    ]
  }

  depends_on = [
    openstack_compute_floatingip_associate_v2.ftp_ip,
    openstack_compute_instance_v2.ftp,
  ]
}


