resource "openstack_compute_instance_v2" "bastion" {
  name              = "${var.env_name}-bastion"
  flavor_name       = var.flavor
  image_name        = var.image
  key_pair          = openstack_compute_keypair_v2.terraform.name

  network {
    uuid = var.network_id
  }

  security_groups = [
    openstack_compute_secgroup_v2.bastion.name,
    "default",
  ]
}

resource "openstack_compute_floatingip_associate_v2" "bastion_ip" {
  floating_ip = openstack_networking_floatingip_v2.bastion_ip.address
  instance_id = openstack_compute_instance_v2.bastion.id
  fixed_ip    = openstack_compute_instance_v2.bastion.network.0.fixed_ip_v4
}

