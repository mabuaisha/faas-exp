# faas-exp
This project is created as part of Thesis in Software Engineering for measuring the performance of Serverless using 3 different container orchestration frameworks (Kubernetes, Docker Swarm, Nomad).
The following items are automated by this tool:

1. Automate infrastructure provisioning on AWS & Openstack
2. Automate deployment Serverless functions on Kubernetes, Docker Swarm, Nomad.
3. Automate test cases generation using Jmeter.  

This project is mainly two parts:
1. Terraform part (Infrastructure + Configuration + Deployment)
2. Python part (faas-exp tool)

## Requirements

In order to run Terraform part you need to have the following:

1. Terraform >= v0.12.21

2. Linux OS (Centos 7.x or Redhat) or MacOS

2. AWS Account or Openstack Account


## Installation

