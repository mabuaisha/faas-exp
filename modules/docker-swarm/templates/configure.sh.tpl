#!/bin/bash
set -e


function setupDocker(){
    echo "Installing Docker..."
    sudo yum install -y yum-utils device-mapper-persistent-data lvm2
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo yum install -y docker-ce-19.03.7-3.el7

    # Restart the docker daemon
    sudo service docker restart
    sudo docker --version
}

function configureDockerAccount(){
 docker login --username="${docker_username}" --password="${docker_password}" 2> /dev/null

}

function setDockerMTU(){
    sudo sed -i "s/\/usr\/bin\/dockerd -H fd:\/\/ --containerd=\/run\/containerd\/containerd.sock/\/usr\/bin\/dockerd --mtu=1450 -H fd:\/\/ --containerd=\/run\/containerd\/containerd.sock/g" /usr/lib/systemd/system/docker.service
    sudo systemctl daemon-reload
    sudo systemctl restart docker
}



# Install and setup docker
setupDocker

# Configure docker auth by providing username/password for dockerhub
configureDockerAccount

# Set MTU to 1450 because of openstack issue network connection
setDockerMTU