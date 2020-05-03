#!/bin/bash

set -e

export MASTER_IP=${MASTER_IP}
export DOCKER_USERNAME=${DOCKER_USERNAME}
export DOCKER_PASSWORD=${DOCKER_PASSWORD}
export DOCKER_EMAIL=${DOCKER_EMAIL}

function configureKubectl(){
 scp -i /home/centos/faas_key.pem -o StrictHostKeyChecking=no centos@$MASTER_IP:/home/centos/admin.conf kubespray-do.conf
 export KUBECONFIG=/home/centos/kubespray-do.conf
}

function configureDockerHub(){
    docker login --username="$DOCKER_USERNAME" --password="$DOCKER_PASSWORD" 2> /dev/null
    kubectl create secret docker-registry dockerhub \
        -n openfaas-fn \
        --docker-username=$DOCKER_USERNAME \
        --docker-password=$DOCKER_PASSWORD \
        --docker-email=$DOCKER_EMAIL
}

function setupIngressController(){
    # Clone kubernetes-ingress controller from nginxinc
    git clone https://github.com/nginxinc/kubernetes-ingress/
    cd kubernetes-ingress/deployments
    git checkout v1.6.3

    # Configure RBAC
    kubectl apply -f common/ns-and-sa.yaml
    kubectl apply -f rbac/rbac.yaml

    # Create the Default Secret, Customization ConfigMap, and Custom Resource Definitions
    kubectl apply -f common/default-server-secret.yaml
    kubectl apply -f common/nginx-config.yaml
    kubectl apply -f common/custom-resource-definitions.yaml

    # Deploy the Ingress Controller
    kubectl apply -f daemon-set/nginx-ingress.yaml

    # Create a Service for the Ingress Controller Pods
    kubectl create -f service/nodeport.yaml
}

function deployOpenFaas(){
 kubectl apply -f https://raw.githubusercontent.com/mabuaisha/faas-netes/master/namespaces.yml

 helm repo add openfaas https://openfaas.github.io/faas-netes/

 helm repo update \
 && helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set functionNamespace=openfaas-fn \
    --set generateBasicAuth=false \
    --set basic_auth=false \
    --set ingress.enabled=true \
    --set faasIdler.dryRun=false \
    --set faasIdler.inactivityDuration=15m

}

configureKubectl

setupIngressController

deployOpenFaas

configureDockerHub
