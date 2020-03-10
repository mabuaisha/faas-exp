#!/bin/bash
set -e

echo "Getting Private IP..."
PRIVATE_IP=$(hostname -I | awk '{print $1}')
CONSUL_HOSTS=%{ for host in consul_hosts ~}"\"${host}"\", %{ endfor ~}

function installPackages() {
  echo "Installing Common Packages..."
  sudo yum install unzip git -y
}

function installDockerEngine() {
    echo "Installing Docker..."
    sudo yum install -y yum-utils device-mapper-persistent-data lvm2
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo yum install -y docker-ce

    # Restart the docker daemon
    sudo service docker restart
    sudo docker --version

}

function configureDockerAccount(){
 docker login --username="${docker_username}" --password="${docker_password}" 2> /dev/null
 sudo cp /home/centos/.docker/config.json /etc/docker-auth.json
 sudo chmod 644 /etc/docker-auth.json

}

function setDockerMTU(){
    sudo sed -i "s/\/usr\/bin\/dockerd -H fd:\/\/ --containerd=\/run\/containerd\/containerd.sock/\/usr\/bin\/dockerd --mtu=1450 -H fd:\/\/ --containerd=\/run\/containerd\/containerd.sock/g" /usr/lib/systemd/system/docker.service
    sudo systemctl daemon-reload
    sudo systemctl restart docker
}

function installConsul() {
  echo "Downloading Consul..."
  cd /tmp
  curl -sLo consul.zip https://releases.hashicorp.com/consul/${consul_version}/consul_${consul_version}_linux_amd64.zip

  echo "Installing Consul..."
  unzip consul.zip >/dev/null
  sudo chmod +x consul
  sudo mv consul /usr/local/bin/consul

  # Setup Consul
  sudo mkdir -p /mnt/consul
  sudo mkdir -p /etc/consul.d
  sudo tee /tmp/config.hcl > /dev/null <<EOF
  ${consul_config}
EOF

  sudo mv /tmp/config.hcl /etc/consul.d/config.hcl
  sudo tee /tmp/consul.service > /dev/null <<"EOF"
  [Unit]
  Description = "Consul"

  [Service]
  # Stop consul will not mark node as failed but left
  KillSignal=INT
  ExecStart=/usr/local/bin/consul agent -config-dir "/etc/consul.d"
  Restart=always
  ExecStopPost=sleep 5
EOF

  sudo mv /tmp/consul.service /etc/systemd/system/consul.service

}


function installNomad() {
  echo "Downloading Nomad..."
  cd /tmp
  curl -sLo nomad.zip https://releases.hashicorp.com/nomad/${nomad_version}/nomad_${nomad_version}_linux_amd64.zip

  echo "Installing Nomad..."
  unzip nomad.zip >/dev/null
  sudo chmod +x nomad
  sudo mv nomad /usr/local/bin/nomad

  # Setup Nomad
  sudo mkdir -p /mnt/nomad
  sudo mkdir -p /etc/nomad.d
  sudo tee /tmp/config.hcl > /dev/null <<EOF
  ${nomad_config}
EOF
  sudo mv /tmp/config.hcl /etc/nomad.d/config.hcl

  # Prepare the service to configure
  sudo tee /tmp/nomad.service > /dev/null <<"EOF"
  [Unit]
  Description = "Nomad"

  [Service]
  # Stop consul will not mark node as failed but left
  KillSignal=INT
  ExecStart=/usr/local/bin/nomad agent -config "/etc/nomad.d"
  Restart=always
  ExecStopPost=sleep 5
EOF

 sudo mv /tmp/nomad.service /etc/systemd/system/nomad.service

}

function install() {
    # Install common software packages
    installPackages

    # Install Consul
    installConsul

    # Install Nomad
    installNomad

# Only Install Docker for client types
%{ if server_type == "client"}
    installDockerEngine
    configureDockerAccount
    setDockerMTU
%{ endif }
}

function startServices(){
    # Start services
    sudo systemctl daemon-reload

    sudo systemctl enable consul.service
    sudo systemctl start consul.service

    sudo systemctl enable nomad.service
    sudo systemctl start nomad.service

}


# Install all required softwares
install

# Start all services
startServices



