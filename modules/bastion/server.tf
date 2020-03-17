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

  provisioner "local-exec" {
    command = "ssh-add ${var.private_key}"
  }
}

resource "openstack_compute_floatingip_associate_v2" "bastion_ip" {
  floating_ip = openstack_networking_floatingip_v2.bastion_ip.address
  instance_id = openstack_compute_instance_v2.bastion.id
  fixed_ip    = openstack_compute_instance_v2.bastion.network.0.fixed_ip_v4
}

resource "null_resource" "bastion_packages" {

  connection {
    host                = openstack_networking_floatingip_v2.bastion_ip.address
    agent               = "true"
    type                = "ssh"
    user                = "centos"
    private_key         = file(var.private_key)
  }

  provisioner "remote-exec" {
    inline = [
      "echo Installing Docker...",
      "sudo yum install -y yum-utils device-mapper-persistent-data lvm2 git",
      "sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo",
      "sudo yum install -y docker-ce-19.03.5-3.el7",
      "sudo usermod -aG docker centos",
      "sudo service docker restart",
      "sudo docker --version",
      "curl -sL https://cli.openfaas.com -o faas.sh",
      "chmod +x faas.sh && ./faas.sh",
      "sudo cp faas-cli /usr/local/bin/faas-cli",
      "sudo ln -sf /usr/local/bin/faas-cli /usr/local/bin/faas",
    ]
  }

  depends_on = [
    openstack_compute_floatingip_associate_v2.bastion_ip,
    openstack_compute_instance_v2.bastion,
  ]
}

