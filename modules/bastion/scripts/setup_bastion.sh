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
sudo yum install -y java-1.8.0-openjdk
sudo yum -y groupinstall "Development Tools"
sudo yum -y install libffi-devel zlib-devel bzip2-devel readline-devel sqlite-devel wget curl llvm ncurses-devel openssl-devel lzma-sdk-devel libyaml-devel redhat-rpm-config gcc

# Install and configure terraform in bastion host
curl https://releases.hashicorp.com/terraform/0.12.21/terraform_0.12.21_linux_386.zip -o terraform.zip
unzip terraform.zip
sudo mv terraform /usr/local/bin/

# Install Jmeter
curl http://www.gtlib.gatech.edu/pub/apache/jmeter/binaries/apache-jmeter-5.2.1.tgz -o apache-jmeter-5.2.1.tgz
tar -xf apache-jmeter-5.2.1.tgz
echo 'export JMETER_HOME=/home/centos/apache-jmeter-5.2.1' >> ~/.bashrc
echo  'export PATH=$JMETER_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

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

# Prepare virtaulenv
# Install pyenv installer so that we can setup it later on
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

echo 'export PATH="$HOME/.pyenv/bin:$PATH"'  >> ~/.bashrc
echo 'eval "$(pyenv init -)"'  >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"'  >> ~/.bashrc

echo "Source bashrc"
source ~/.bashrc

# Setup pyenv
echo "Setup Pyenv is done !!!"
pyenv --version

echo "Install python version 3.7.0"
pyenv install 3.7.0

echo "Create virtualenv called k8s"
pyenv virtualenv 3.7.0 faas