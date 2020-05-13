output "floating_ip" {
  value = aws_eip_association.bastion_eip_association.public_ip
}