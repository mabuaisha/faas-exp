resource "null_resource" "cluster" {
  connection {
    host = var.bastion_ip
    agent = "true"
    type = "ssh"
    user = "centos"
    private_key = file(var.private_key)
  }

  provisioner "file" {
    source = "${path.module}/scripts/setup.sh"
    destination = "/home/centos/setup.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /home/centos/setup.sh",
      "/home/centos/setup.sh",
    ]
  }
}