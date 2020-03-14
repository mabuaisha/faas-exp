resource "openstack_compute_servergroup_v2" "server_group" {
  name = var.server_group
  policies = var.server_group_policies
}

resource "openstack_compute_instance_v2" "master" {
  count             = var.master_count
  name              = "${var.env_name}-master-${var.worker_name}-${count.index}"
  flavor_name       = var.server_flavor
  image_name        = var.server_image
  key_pair          = "${var.env_name}-keypair"

  scheduler_hints {
    group = openstack_compute_servergroup_v2.server_group.id
  }

  network {
    uuid = var.network_id
  }

  security_groups = [var.security_group_ids]

}

resource "openstack_compute_instance_v2" "worker" {
  count             = var.worker_count
  name              = "${var.env_name}-worker-${var.worker_name}-${count.index}"
  flavor_name       = var.server_flavor
  image_name        = var.server_image
  key_pair          = "${var.env_name}-keypair"

  scheduler_hints {
    group = openstack_compute_servergroup_v2.server_group.id
  }

  network {
    uuid = var.network_id
  }

  security_groups = [var.security_group_ids]

}

resource "null_resource" "inventory" {
  connection {
    host = var.bastion_ip
    agent = "true"
    type = "ssh"
    user = "centos"
    private_key = file(var.private_key)
  }

  provisioner "file" {
    content = templatefile("${path.module}/templates/inventory.yml.tpl",
    {
      worker_ips = openstack_compute_instance_v2.worker.*.network.0.fixed_ip_v4
      master_ips = openstack_compute_instance_v2.master.*.network.0.fixed_ip_v4
    }
    )
    destination     = "/home/centos/inventory.yml"
  }

  depends_on = [openstack_compute_instance_v2.worker, openstack_compute_instance_v2.master]

}

//resource "null_resource" "cluster" {
//  connection {
//    host = var.bastion_ip
//    agent = "true"
//    type = "ssh"
//    user = "centos"
//    private_key = file(var.private_key)
//  }
//
//  provisioner "file" {
//    source = "${path.module}/scripts/setup.sh"
//    destination = "/home/centos/setup.sh"
//  }
//
//  provisioner "remote-exec" {
//    inline = [
//      "chmod +x /home/centos/setup.sh",
//      "/home/centos/setup.sh",
//    ]
//  }
//}