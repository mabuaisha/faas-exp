#!/bin/bash

set -e


function configureKubectl(){
 scp -i ~/.ssh/faas_key.pem -o StrictHostKeyChecking=no centos@$MASTER_IP:/home/centos/admin.conf kubespray-do.conf
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
    --set generateBasicAuth=true

 PASSWORD=$(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
}

configureKubectl

deployOpenFaas

configureDockerHub