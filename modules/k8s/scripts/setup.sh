#!/bin/bash

set -e


function setupVirtualenv(){
 # Install pyenv installer so that we can setup it later on
 curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

 echo 'export PATH="$HOME/.pyenv/bin:$PATH"'  >> ~/.bashrc
 echo 'eval "$(pyenv init -)"'  >> ~/.bashrc
 echo 'eval "$(pyenv virtualenv-init -)"'  >> ~/.bashrc

 source ~/.bashrc

 # Setup pyenv
 pyenv --version
 pyenv install 3.7.0
 pyenv virtualenv 3.7.0 k8s

}


function installPackages(){
 # install common development tool in centos machine
 sudo yum -y groupinstall "Development Tools"
 sudo yum -y install libffi-devel zlib-devel bzip2-devel readline-devel sqlite-devel wget curl llvm ncurses-devel openssl-devel lzma-sdk-devel libyaml-devel redhat-rpm-config
 sudo yum -y install git

 cat <<EOF > /etc/yum.repos.d/kubernetes.repo
 [kubernetes]
 name=Kubernetes
 baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
 enabled=1
 gpgcheck=1
 repo_gpgcheck=1
 gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
 EOF

 sudo yum install -y kubectl

}

function prepareKubespray(){
  git clone git@github.com:kubernetes-sigs/kubespray.git
  cd kubespray

  pyenv activate k8s

  pip install -r requirements.txt

  pyenv deactivate


}

# Install Packages
installPackages

# Setup Virtualenv
setupVirtualenv

# Prepare Kubespary
prepareKubespray

