resource "openstack_compute_servergroup_v2" "server_group" {
  name     = var.server_group
  policies = var.server_group_policies
}

resource "openstack_compute_instance_v2" "server" {
  count             = var.worker_count
  name              = "${var.env_name}-${var.worker_name}-${count.index}"
  flavor_name       = var.worker_flavor
  image_name        = var.worker_image
  key_pair          = "${var.env_name}-keypair"

  scheduler_hints {
    group             = openstack_compute_servergroup_v2.server_group.id
  }


  network {
    uuid = var.network_id
  }

  security_groups = var.security_group_ids

}

