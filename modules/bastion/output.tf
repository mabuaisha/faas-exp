output "bastion-instance-floating-ip" {
  value = openstack_networking_floatingip_v2.bastion_ip.address
}


