datacenter = "${datacenter}"
data_dir = "/tmp/consul"
bind_addr = "0.0.0.0"

advertise_addr = "$PRIVATE_IP"
advertise_addr_wan = "$PRIVATE_IP"
addresses {
  http = "0.0.0.0"
}

disable_remote_exec = true
disable_update_check = true
leave_on_terminate = true

retry_join = [$CONSUL_HOSTS]

server = false