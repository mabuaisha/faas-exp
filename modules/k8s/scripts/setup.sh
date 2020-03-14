#!/bin/bash

set -e

function installPackages(){
 # install common development tool in centos machine
 sudo yum groupinstall "Development Tools"
 sudo yum install libffi-devel zlib-devel bzip2-devel readline-devel sqlite-devel wget curl llvm ncurses-devel openssl-devel lzma-sdk-devel libyaml-devel redhat-rpm-config

 # Install pyenv installer so that we can setup it later on
 curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

echo 'export PATH="$HOME/.pyenv/bin:$PATH"'  >> ~/.bashrc
echo 'eval "$(pyenv init -)"'  >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"'  >> ~/.bashrc

source ~/.bashrc

pyenv --version

pyenv install 3.7.0

pyenv virtualenv 3.7.0 k8s


pyenv activate k8s

}

installPackages