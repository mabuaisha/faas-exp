#!/bin/bash

set -e

export MASTER_IP=${MASTER_IP}
export DOCKER_USERNAME=${DOCKER_USERNAME}
export DOCKER_PASSWORD=${DOCKER_PASSWORD}
export DOCKER_EMAIL=${DOCKER_EMAIL}

function configureKubectl(){
 scp -i /home/centos/faas_key.pem -o StrictHostKeyChecking=no centos@$MASTER_IP:/home/centos/admin.conf kubespray-do.conf
 export KUBECONFIG=$PWD/kubespray-do.conf
}

function configureDockerHub(){
    kubectl create secret docker-registry dockerhub \
        -n openfaas-fn \
        --docker-username=$DOCKER_USERNAME \
        --docker-password=$DOCKER_PASSWORD \
        --docker-email=$DOCKER_EMAIL
}

function deployOpenFaas(){
 kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml

 helm repo add openfaas https://openfaas.github.io/faas-netes/

 helm repo update \
 && helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set functionNamespace=openfaas-fn \
    --set generateBasicAuth=true \
    --set faasIdler.dryRun=false

 PASSWORD=$(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)

 echo "OpenFaaS admin password: $PASSWORD"
}

configureKubectl

deployOpenFaas

configureDockerHub