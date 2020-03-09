data_dir = "/tmp/consul"
datacenter = "${datacenter}"

ui = true
# Set this as server
server = true

# For now will make consule server as only one instance
bootstrap_expect = ${instances}
retry_join = [$CONSUL_HOSTS]

advertise_addr = "$PRIVATE_IP"
advertise_addr_wan = "$PRIVATE_IP"

addresses = {
  http = "0.0.0.0"
}