#!/bin/bash

set -e

# Activate ssh agent process
eval "$(ssh-agent -s)"

# Install required packages including docker, git, ab
echo "Installing Docker..."
sudo yum install -y yum-utils device-mapper-persistent-data lvm2 git
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce-19.03.7-3.el7
sudo yum install -y httpd-tools
sudo yum install -y unzip

# Install and configure terraform in bastion host
curl https://releases.hashicorp.com/terraform/0.12.21/terraform_0.12.21_linux_386.zip -o terraform.zip
unzip terraform.zip
sudo mv terraform /usr/local/bin/

# Config docker
sudo usermod -aG docker centos
sudo service docker restart
sudo docker --version
sudo sed -i "s/\/usr\/bin\/dockerd -H fd:\/\/ --containerd=\/run\/containerd\/containerd.sock/\/usr\/bin\/dockerd --mtu=1450 -H fd:\/\/ --containerd=\/run\/containerd\/containerd.sock/g" /usr/lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo systemctl restart docker

# Config and install faas cli on the bastion client
curl -sL https://cli.openfaas.com -o faas.sh
chmod +x faas.sh && ./faas.sh
sudo cp faas-cli /usr/local/bin/faas-cli
sudo ln -sf /usr/local/bin/faas-cli /usr/local/bin/faas