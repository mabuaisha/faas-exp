all:
  hosts:
  %{ for index, ip in worker_ips ~}
    node${index}:
      ansible_host: ${ip}
      ip: ${ip}
      access_ip: ${ip}
  %{ endfor ~}
  %{ for index, ip in master_ips ~}
    master${index}:
      ansible_host: ${ip}
      ip: ${ip}
      access_ip: ${ip}
  %{ endfor ~}
  children:
    kube-master:
      hosts:
      %{ for index, ip in master_ips ~}
        master${index}:
          ansible_host: ${ip}
          ip: ${ip}
          access_ip: ${ip}
      %{ endfor ~}
    kube-node:
      hosts:
      %{ for index, ip in worker_ips ~}
        node${index}:
      %{ endfor ~}
    etcd:
      hosts:
      %{ for index, ip in master_ips ~}
        master${index}:
          ansible_host: ${ip}
          ip: ${ip}
          access_ip: ${ip}
      %{ endfor ~}
    k8s-cluster:
      children:
        kube-master:
        kube-node:
    calico-rr:
      hosts: {}