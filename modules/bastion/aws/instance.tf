resource "aws_instance" "bastion" {
  ami                    = data.aws_ami.bastion_ami.id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.terraform.key_name
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.bastion.id]
  tags {
    Name = "${var.env_name}-bastion"
  }
  root_block_device {
    volume_size = var.volume_size
    delete_on_termination = true
  }
  depends_on = [aws_security_group.bastion]
}

resource "aws_eip" "bastion_eip" {
  vpc      = true
  depends_on = [aws_instance.bastion]
}

resource "aws_eip_association" "bastion_eip_association" {
  instance_id   = aws_instance.bastion.id
  allocation_id = aws_eip.bastion_eip.id
  depends_on = [aws_eip.bastion_eip, aws_instance.bastion]
}

resource "null_resource" "bastion_packages" {

  connection {
    host                = aws_eip_association.bastion_eip_association.public_ip
    agent               = "true"
    type                = "ssh"
    user                = "centos"
    private_key         = file(var.private_key)
  }

  provisioner "file" {
   source = "${path.module}/scripts/setup_bastion.sh"
   destination = "/home/centos/setup_bastion.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /home/centos/setup_bastion.sh",
      "/home/centos/setup_bastion.sh",
    ]
  }

  depends_on = [
    aws_eip_association.bastion_eip_association,
    aws_instance.bastion,
  ]
}
