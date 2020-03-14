#!/bin/bash

set -e


function setupVirtualenv(){
 # Install pyenv installer so that we can setup it later on
 curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

 echo 'export PATH="$HOME/.pyenv/bin:$PATH"'  >> ~/.bashrc
 echo 'eval "$(pyenv init -)"'  >> ~/.bashrc
 echo 'eval "$(pyenv virtualenv-init -)"'  >> ~/.bashrc

 source ~/.bashrc

 exec $SHELL

 # Setup pyenv
 pyenv --version
 pyenv install 3.7.0
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

   setupOpenfaas

}

function prepareKubespray(){
  git clone https://github.com/kubernetes-sigs/kubespray.git
  cd kubespray

  source ~/.bashrc

  pyenv activate k8s

  pip install -r requirements.txt

  pyenv deactivate

}

function setupK8SCluster(){
  echo "Run cluster"
}

function deployOpenfaas(){
 echo "Run OpenFaas"
}

# Install Packages
installPackages

# Setup Virtualenv
setupVirtualenv

# Prepare Kubespary
prepareKubespray

# Setup cluster
setupK8SCluster

# Deploy OpenFaas
deployOpenfaas