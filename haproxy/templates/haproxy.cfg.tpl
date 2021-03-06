global
    log     127.0.0.1 local2

    chroot  /var/lib/haproxy
    pidfile   /var/run/haproxy.pid
    maxconn   4000
    user      haproxy
    group     haproxy
    daemon

    # turn on stats unix socket
    stats socket /var/lib/haproxy/stats

defaults
  mode http
  timeout client 30m
  timeout connect 5m
  timeout server 30m
  timeout check 5m


frontend http_front
  bind *:80
  default_backend http_backend

frontend http_front_alert_manager
  bind *:5000
  use_backend alert_manager

frontend stats
    bind *:9000
    stats enable
    stats uri /haproxy/stats

backend alert_manager
  balance roundrobin
  http-request set-header Host prometheus.openfaas.local
  %{ for index, ip in backend_ips}
    server worker_${index} ${ip}:${prometheus_backend_port}
  %{ endfor}


backend http_backend
  balance roundrobin
  http-request set-header Host gateway.openfaas.local
  %{ for index, ip in backend_ips}
    server worker_${index} ${ip}:${openfaas_backend_port}
  %{ endfor}