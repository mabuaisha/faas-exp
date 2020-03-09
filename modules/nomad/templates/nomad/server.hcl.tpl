datacenter = "${datacenter}"
data_dir  = "/tmp/nomad"

bind_addr = "0.0.0.0" # the default


advertise {
  # Defaults to the node's hostname. If the hostname resolves to a loopback
  # address you must manually configure advertise addresses.
  http = "$PRIVATE_IP"
  rpc  = "$PRIVATE_IP"
  serf = "$PRIVATE_IP:5648" # non-default ports may be specified
}

server {
  enabled          = true
  bootstrap_expect = ${instances}
}


consul {
  address = "$PRIVATE_IP:8500"

  server_service_name = "nomad"
  client_service_name = "nomad-client"

  # Enables automatically registering the services.
  auto_advertise = true

  # Enabling the server and client to bootstrap using Consul.
  server_auto_join = true
  client_auto_join = true
}