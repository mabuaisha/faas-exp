#!/bin/bash

set -e


function setupVirtualenv(){
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
 pyenv virtualenv 3.7.0 k8s

}


function setupCommonPackages(){
 # install common development tool in centos machine
 sudo yum -y groupinstall "Development Tools"
 sudo yum -y install libffi-devel zlib-devel bzip2-devel readline-devel sqlite-devel wget curl llvm ncurses-devel openssl-devel lzma-sdk-devel libyaml-devel redhat-rpm-config
 sudo yum -y install git
}

function setupHelm(){
 curl -sSLf https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
}

function setupKubectl() {
  curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.17.0/bin/linux/amd64/kubectl
  chmod +x ./kubectl
  sudo mv ./kubectl /usr/local/bin/kubectl
  kubectl version --client
}

function setupOpenfaas(){
  curl -sL https://cli.openfaas.com -o faas.sh
  chmod +x faas.sh && ./faas.sh
  sudo cp faas-cli /usr/local/bin/faas-cli
  sudo ln -sf /usr/local/bin/faas-cli /usr/local/bin/faas
}

function installPackages(){
   setupCommonPackages

   setupHelm

   setupKubectl

   #setupOpenfaas

}

function prepareKubespray(){
  git clone https://github.com/kubernetes-sigs/kubespray.git
  pushd kubespray
    git checkout v2.11.2
    source ~/.bashrc
    pyenv activate k8s
    pip install -r requirements.txt
    pyenv deactivate
  popd
}

function setupK8SCluster(){
  echo "Start installing cluster....."
  source ~/.bashrc
  pushd kubespray
    # Enable virtualenv
    pyenv activate k8s
    # Run ansible cluster
    ansible-playbook -i /home/centos/inventory.yml -u centos -b --key-file=~/.ssh/faas_key.pem cluster.yml -e docker_version=19.03
    # Deactivate virtualenv
    pyenv deactivate
  popd
}

# Install Packages
installPackages

# Setup Virtualenv
setupVirtualenv

# Prepare Kubespary
prepareKubespray

# Setup cluster
setupK8SCluster