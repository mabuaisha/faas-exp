# faas-exp
This project is created as part of Thesis in Software Engineering for measuring the performance of Serverless using 3 different container orchestration frameworks (Kubernetes, Docker Swarm, Nomad) where Openfass framework is used as a use case.
The following items are automated by this project:

1. Automate infrastructure provisioning on AWS & Openstack cloud.
2. Automate deployment Serverless functions on Kubernetes, Docker Swarm, Nomad.
3. Automate test cases generation.  

This project is mainly has two parts:
1. Infrastructure provisioning, clusters setup and serverless framework deployment.
2. Experiment runner

## Part1

This part focus on infrastructure provisioning, configuration and serverless framework deployment where two cloud providers are supported (AWS & Openstack).

### Prerequisites 

In order to be able to setup part1 the following items are needed:

1. [Terraform](https://releases.hashicorp.com/terraform/0.12.21/)

2. Setup one of the Public Cloud API credentials:

    - AWS by creating file `.env` file  and source it `source .env`
    
        ```
        export AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXXXXXXX"
        export AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXXXXXX"
        export AWS_DEFAULT_REGION="us-east-1"

        ```
    - Download Openstack API v3 RC file from the Openstack Horizon and source it `source YOUR-OPENSTACK-PROVIDERE-openrc.sh`

2. Linux OS Centos 7.x (with user "centos")

### Terraform files

This project has terraform files for the following resources:

1. [Bastion](/bastion)
2. [Docker Swarm](/docker-swarm)
3. [Nomad](/nomad)
4. [Kubernetes](/k8s)
5. [HAproxy](/haproxy)
6. [FTP](/ftp)


#### Bastion

Bastion is created as jumphost that helps to create all other resources and run the experiment as it is the only resource has a public ip address and all other has private ip addresses. where the following resources get created

1. VPC
2. Public Subnet
3. Private Subnet
4. Internet Gateway
5. NAT Gateway
6. Routing Tables
7. KeyPair


##### AWS

The following inputs are used to create bastion resource on AWS as specified on the [variables](/bastion/aws/variables.tf) file:

- `availability_zone`: Availability zone. The default value is `us-east-1b`.
- `vpc_cidr`: The VPC cidr. The default value is `10.0.0.0/16`.
- `public_subnet_cidr`: The public subnet cidr. The default `10.0.1.0/24`.
- `private_subnet_cidr`: The private subnet cidr. The default `10.0.2.0/24`.
- `public_key`: The public key required to attach for keypair. The default location `~/.ssh/faas_ssh.pub`.
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `volume_size`: The volume size for bastion instance. The default value is `15` GB.
- `instance_type`: The instance type for AWS. The default value is `t3a.medium`.
- `image_id`: The image id where instance is creating from. The default value is `ami-0affd4508a5d2481b` (Centos 7.6) 


Note: The generation for the both private and public keys can be done using 
```
    ssh-keygen -t rsa -b 4096 -C "youremail@domain.com"
```

To create bastion update your variables file and run the following command inside [aws](/bastion/aws):

```
terraform init
terraform apply

```

Terraform outputs
```
floating_ip = "19.210.11.20"
vpc_id = 'vpc-0a2d1c0a512011a42
subnet_id = "subnet-0a6d2c0a513011a42"
security_group_ids = ["sg-168975527090df7c4"]
```

##### Openstack

The following inputs are used to create bastion resource on Openstack as specified on the [variables](/bastion/openstack/variables.tf) file:

- `external_network_name`: External network name. Required field its based on the Openstack provider could be (ext, ext-net, ..etc).
- `flavor`: The type of the machine need to be created. (Required) Flavor is a custom in Openstack and varies from provider to provider.
- `image`: The image type where instance is going to be created. (Required) This project use Centos and the name varies from from provider to provider.
- `public_key`: The public key required to attach for keypair. The default location `~/.ssh/faas_ssh.pub`.
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `subnet_cidr`: The subnet cidr. The default `192.168.0.0/24`.
- `dns_nameservers`: An array of DNS name server names used by hosts in this subnet. The default `["8.8.8.8", "8.8.4.4"]`.


Note: The generation for the both private and public keys can be done using 
```
    ssh-keygen -t rsa -b 4096 -C "youremail@domain.com"
```

To create bastion update your variables file and run the following command inside [aws](/bastion/aws):

```
terraform init
terraform apply -var-file=inputs.tfvars

```

`inputs.tfvars` should be created to fill the required values and override any default value.

Terraform outputs
```
floating_ip = "18.222.12.12"
network_id = '2fc090f1-b00a-4ac6-be40-251w4b184471
```

#### Docker Swarm

This module is used to create required resources for docker swarm which includes at least 3 machines: 1 manager + 2 workers.

The current Terraform code support creating only 1 manager and multiple workers and in future we are going to update the code to support creating multiple managers. 

Notes: 
1. Make sure [jq](https://stedolan.github.io/jq/) is installed on the machine that execute terraform.
2. Make sure the ssh agent is up and running `eval "$(ssh-agent -s)"`
3. Make sure to add your private key to the ssh-agent `ssh-add ~/.ssh/faas_ssh`


##### AWS

The following inputs are used to create docker swarm resource on AWS as specified on the [variables](/docker-swarm/aws/variables.tf) file:

- `subnet_id`: The private subent id. Required.
- `bastion_ip`: The bastion ip. Required.
- `docker_username`: The dockerhub username. Required
- `docker_password`: The dockerhub password. Required
- `security_group_ids`: The list of security group ids. Required
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `worker_name`: The worker name. The default value is `docker-swarm`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `manager_count`: The number of managers. The default value is `1` and should be 1.
- `worker_count`: The number of workers. The default value is `2`.
- `volume_size`: The volume size for bastion instance. The default value is `15` GB.
- `instance_type`: The instance type for AWS. The default value is `t3a.large`.
- `image_id`: The image id where instance is creating from. The default value is `ami-0affd4508a5d2481b` (Centos 7.6)  

To create bastion update your variables file and run the following command inside [aws](/bastion/aws):


##### Openstack

The following inputs are used to create docker swarm resource resource on Openstack as specified on the [variables](/docker-swarm/openstack/variables.tf) file:

- `network_id`:The network id where bastion resourced created in. Required.
- `bastion_ip`: The bastion ip. Required.
- `docker_username`: The dockerhub username. Required
- `docker_password`: The dockerhub password. Required
- `flavor`: The type of the machine need to be created. (Required) Flavor is a custom in Openstack and varies from provider to provider.
- `image`: The image type where instance is going to be created. (Required) This project use Centos and the name varies from from provider to provider.
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `worker_name`: The worker name. The default value is `docker-swarm`.
- `manager_count`: The number of managers. The default value is `1` and should be 1.
- `worker_count`: The number of workers. The default value is `2`.


For both AWS & Openstack run the following commands:

```
terraform init
terraform apply -var-file=inputs.tfvars

```

`inputs.tfvars` should be created to fill the required values and override any default value.

Terraform outputs
```
worker-ips = [10.0.2.111, 10.0.2.130]
manager-ips = [10.0.2.112]
worker_token = SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c
manager_token =49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c 
```

#### Nomad

This module is used to create required resources for nomad and deploy OpenFaas Serverless framework to the cluster which includes 3 machines: 1 server and 2 clients.

For the sake of this study the current version of this project supports 3 nodes (1 server + 2 clients) and its going to be updated in near future.

##### AWS

The following inputs are used to create nomad resource resource on AWS as specified on the [variables](/nomad/aws/variables.tf) file:

- `subnet_id`: The private subent id. Required.
- `bastion_ip`: The bastion ip. Required.
- `docker_username`: The dockerhub username. Required
- `docker_password`: The dockerhub password. Required
- `security_group_ids`: The list of security group ids. Required
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `worker_name`: The worker name. The default value is `nomad`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `servers_count`: The number of nomad servers. The default value is `1` and should be 1.
- `clients_count`: The number of clients. The default value is `2`.
- `volume_size`: The volume size for bastion instance. The default value is `15` GB.
- `instance_type`: The instance type for AWS. The default value is `t3a.large`.
- `image_id`: The image id where instance is creating from. The default value is `ami-0affd4508a5d2481b` (Centos 7.6)
- `datacenter`: The data center value for nomad. The default value is `dc1`.
- `consul_version`: The consul version used for this experiment. The default value is `1.2.0`.
- `nomad_version`: The nomad version used for this experiment. The default value is `0.8.4`.  


##### Openstack

The following inputs are used to create nomad resource resource on Openstack as specified on the [variables](/nomad/openstack/variables.tf) file:

- `network_id`:The network id where bastion resourced created in. Required.
- `bastion_ip`: The bastion ip. Required.
- `docker_username`: The dockerhub username. Required
- `docker_password`: The dockerhub password. Required
- `flavor`: The type of the machine need to be created. (Required) Flavor is a custom in Openstack and varies from provider to provider.
- `image`: The image type where instance is going to be created. (Required) This project use Centos and the name varies from from provider to provider.
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `worker_name`: The worker name. The default value is `nomad`.
- `servers_count`: The number of nomad servers. The default value is `1` and should be 1.
- `clients_count`: The number of clients. The default value is `2`.
- `datacenter`: The data center value for nomad. The default value is `dc1`.
- `consul_version`: The consul version used for this experiment. The default value is `1.2.0`.
- `nomad_version`: The nomad version used for this experiment. The default value is `0.8.4`.

For both AWS & Openstack run the following commands:

```
terraform init
terraform apply -var-file=inputs.tfvars

```

`inputs.tfvars` should be created to fill the required values and override any default value.

Terraform outputs
```
server-ips = [10.0.2.111]
client-ips = [10.0.2.112, 10.0.2.130]
```

#### Kubernetes

This module is used in order to create k8s cluster and deploy OpenFaas Serverless chart to the cluster. The k8s cluster is 1 master and 2 node workers.
 
##### AWS

The following inputs are used to create k8s resource resource on AWS as specified on the [variables](/k8s/aws/variables.tf) file:

- `subnet_id`: The private subent id. Required.
- `bastion_ip`: The bastion ip. Required.
- `docker_username`: The dockerhub username. Required
- `docker_password`: The dockerhub password. Required
- `docker_email`: The dockerhub email. Required
- `security_group_ids`: The list of security group ids. Required
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `worker_name`: The worker name. The default value is `k8s`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `master_count`: The number of k8s master. The default value is `1`.
- `worker_count`: The number of clients. The default value is `2`.
- `volume_size`: The volume size for bastion instance. The default value is `15` GB.
- `instance_type`: The instance type for AWS. The default value is `t3a.large`.
- `image_id`: The image id where instance is creating from. The default value is `ami-0affd4508a5d2481b` (Centos 7.6)


##### Openstack

The following inputs are used to create k8s resource resource on Openstack as specified on the [variables](/k8s/openstack/variables.tf) file:

- `network_id`:The network id where bastion resourced created in. Required.
- `bastion_ip`: The bastion ip. Required.
- `docker_username`: The dockerhub username. Required
- `docker_password`: The dockerhub password. Required
- `docker_email`: The dockerhub email. Required
- `flavor`: The type of the machine need to be created. (Required) Flavor is a custom in Openstack and varies from provider to provider.
- `image`: The image type where instance is going to be created. (Required) This project use Centos and the name varies from from provider to provider.
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `worker_name`: The worker name. The default value is `k8s`.

For both AWS & Openstack run the following commands:

```
terraform init
terraform apply -var-file=inputs.tfvars

```

`inputs.tfvars` should be created to fill the required values and override any default value.

Terraform outputs
```
master-ips = [10.0.2.111]
worker-ip = [10.0.2.112, 10.0.2.130]
```

#### HAProxy

This module is used to create HAProxy as Load balancer to forward the requests to the desired cluster.

The Openfaas Gateway IP will represent the HAProxy IP and from there the Load balancer will forward the requests.

##### AWS

The following inputs are used to create HAProxy resource resource on AWS as specified on the [variables](/haproxy/aws/variables.tf) file:

- `subnet_id`: The private subent id. Required.
- `bastion_ip`: The bastion ip. Required.
- `backend_ips`: The list of backend ips that HAProxy will forward requests to. Usually is the list of workers. Required
- `security_group_ids`: The list of security group ids. Required
- `openfaas_backend_port`: The port that Openfaas gateway listen. The default value is 8080 Except k8s it will be 80.
- `prometheus_backend_port`: The port that prometheus listen to. The default value is 9000. 
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `volume_size`: The volume size for bastion instance. The default value is `12` GB.
- `instance_type`: The instance type for AWS. The default value is `t3a.medium`.
- `image_id`: The image id where instance is creating from. The default value is `ami-0affd4508a5d2481b` (Centos 7.6)


##### Openstack 

The following inputs are used to create HAProxy resource resource on Openstack as specified on the [variables](/haproxy/openstack/variables.tf) file:

- `network_id`:The network id where bastion resourced created in. Required.
- `bastion_ip`: The bastion ip. Required.
- `backend_ips`: The list of backend ips that HAProxy will forward requests to. Usually is the list of workers. Required
- `openfaas_backend_port`: The port that Openfaas gateway listen. The default value is 8080 Except k8s it will be 80.
- `prometheus_backend_port`: The port that prometheus listen to. The default value is 9000. 
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `flavor`: The type of the machine need to be created. (Required) Flavor is a custom in Openstack and varies from provider to provider.
- `image`: The image type where instance is going to be created. (Required) This project use Centos and the name varies from from provider to provider.

For both AWS & Openstack run the following commands:

```
terraform init
terraform apply -var-file=inputs.tfvars

```

`inputs.tfvars` should be created to fill the required values and override any default value.

Terraform outputs
```
private_ip = 10.0.2.109]
```

#### FTP

This module is used in order to create and prepare ftp server that is going to be used by the experiment.

##### AWS

The following inputs are used to create FTP resource on AWS as specified on the [variables](/ftp/aws/variables.tf) file:

- `subnet_id`: The private subent id. Required.
- `bastion_ip`: The bastion ip. Required.
- `security_group_ids`: The list of security group ids. Required
- `ftp_username`: The ftp username to create for access ftp server. The default value is `ftpuser`.
- `ftp_password`: The ftp password to create for access ftp server. The default value is `ftppassword`.
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `volume_size`: The volume size for bastion instance. The default value is `15` GB.
- `instance_type`: The instance type for AWS. The default value is `t3a.medium`.
- `image_id`: The image id where instance is creating from. The default value is `ami-0affd4508a5d2481b` (Centos 7.6)


##### Openstack

The following inputs are used to create FTP resource on Openstack as specified on the [variables](/ftp/openstack/variables.tf) file: 

- `network_id`:The network id where bastion resourced created in. Required.
- `bastion_ip`: The bastion ip. Required.
- `ftp_username`: The ftp username to create for access ftp server. The default value is `ftpuser`.
- `ftp_password`: The ftp password to create for access ftp server. The default value is `ftppassword`.
- `private_key`: The private key required to ssh for instances. The default location `~/.ssh/faas_ssh`.
- `env_name`: The environment name. The default value is `serverless-env`.
- `flavor`: The type of the machine need to be created. (Required) Flavor is a custom in Openstack and varies from provider to provider.
- `image`: The image type where instance is going to be created. (Required) This project use Centos and the name varies from from provider to provider.

For both AWS & Openstack run the following commands:

```
terraform init
terraform apply -var-file=inputs.tfvars

```

`inputs.tfvars` should be created to fill the required values and override any default value.

Terraform outputs
```
private_ip = 10.0.2.109]
```

Notes:
1. Before start using the ftp server, at least add one file to the ftp server called 'test.txt' as it used by the [ftpfunction](/functions/computation-scenarios/network/ftpfunction)
2. The Flavor for openstack option should match the following:
    - 2vCPU + 8GB for cluster resources
    - 2vCPU + 4GB for both FTP + Haproxy + Bastion


## Part2

This part is the one responsible for conducting experiment on specified container orchestrators. Where each experiment represent running all test cases in single orchestrator.

### Prerequisites

1. Make ssh connection to the bastion `ssh -i ~/.ssh/faas_sh centos@BASTION_IP`
2. Run `pyenv activate faas` Where the pyenv and virtaulenv created as part of bastion setup.
3. Clone `faas-exp` repository `git clone https://github.com/mabuaisha/faas-exp.git`
4. Change directory to `faas-exp`
5. Edit the `/etc/hosts` bu adding HAProxy IP that should map to the following domain:
    - gateway.openfaas.local
    - prometheus.openfaas.local
6. Set the following environment variables:
    - `export OPENFAAS_URL="http://gateway.openfaas.local"`.
    - `export KUBECONFIG=/home/centos/kubespray-do.conf` Only relevant for k8s experiment.   
7. Install all python requirements using `pip install -e .`
8. Make sure to pull the latest template by running the following command inside `faas-exp` `faas-cli template pull https://github.com/mabuaisha/templates.git`
9. Make sure that your application is setup correctly by invoking `faas-exp` you should see something like this:

```
(faas-exp) ➜  faas-exp git:(master) ✗ faas-exp
Usage: faas-exp [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  run
  validate

```

The `faas-exp` supports the following command:
1. `faas-exp validate`. This command will validate that your ready to run your experiment.
2. `faas-exp run -c config.yaml`. This command will start running actual experiment.
3. `faas-exp aggregate -s SOURCE_RESULT_DIR -d DESTINATION_RESULT_DIR -e [FUNCTION_NAME]`

### Configuration

The faas-exp tool support configure the experiment for each container orchestrator using yaml config file.

All the configurations for the three container orchestrators are located under [config](/config) section. As the following configuration files are existed:
1. k8s.yaml
2. nomad.yaml
3. swarm.yaml


All of the above configurations need to be edited as they contains some configuration related to HAProxy IP.

The configuration file contains two main section which are:
1. experiment
2. functions

#### Experiment Configuration

Under the `experiment` the following configurations are used:

- `server`: The server endpoint that serve the requests for OpenFaas Serverless and this is represent reference to the HAproxy. Default value is `gateway.openfaas.local`
- `port`: The port on which HAProxy listen for incoming request. The default value is `80`
- `number_of_runs`: The number of runs for each functions. How many time we need to run each function. The default value is `6`.
- `number_of_requests`: The total number of HTTP requests intend to send to the OpenFaas Serverless. Default value is `35000`
- `delay_between_runs`: The number of minutes to delay between each run. The defauly is `1`. 
- `replicas`: The number of replicas to use in case the auto scaling is disable on the OpenFaas Serverless framework for each function. Default values are:
    - 1
    - 10
    - 20
- `concurrency`: The number of simulated users that are going to trigger all the deployed functions.  Default values are:
    - 5
    - 10
    - 20
    - 50 
- `result_dir`: The directory where all the results are going to be dumped. The default value is `/home/centos/result`


Example of experiment configuration

```
experiment:
  server: gateway.openfaas.local
  port: 80
  number_of_runs: 6
  number_of_requests: 35000
  delay_between_runs: 1
  replicas:
    - 1
    - 10
    - 20
  concurrency:
    - 5
    - 10
    - 20
    - 50
  result_dir: /home/centos/result

```


#### Functions Configuration

The functions configuration contains list of all functions that are going to be deployed to the one of the container orchestrators.

All the configuration will be under `functions` section where each function represent an item and the function can contains the following configureation:

- `name`: The name of the function need to be uploaded. For example `warmfunction`
- `yaml_path`: The yaml path file where the openfaas function yaml config is located. For example `functions/warm-starts-scenarios/k8s/warmfunction.yml`
- `environment`: Set of environment variables which are used by the deployed functions. Example of these varaibles:
    - `read_timeout`: The read timeout period. default `5m5s`
    - `write_timeout`: The write timeout period. default `5m5s`
    - `gateway_endpoint`: The gateway endpoint. This is only relevant for composite functions
    - `ftp_host`: The ftp host IP. This is relevant only for network function
    - `ftp_user`: The ftp username. This is relevant only for network function. Default value is `ftpuser`
    - `ftp_password`: The ftp username. This is relevant only for network function. Default value is `ftppassword`
- `api`: The configuration related to function calls which contains the following:
    - `uri`: The uri for called function. For example `function/ftpfunction`
    - `http_method`: The http request method. Default `POST`.
    -  `param`: The min and max values for param passed to the url. Relevant only for matrix, composite functions as the values generated randomly between min and max
           `min`: The min value need to set for the param
           `max`: The max value need to set for the param
- `inactivity_duration`: This is only relevant for cold/warm start function. How many seconds to wait before sending the next request chunk. The default is 5m and it should not be less than 5.
- `chunks_number`: How many chunks you need to send the request to the endpoint. Default value is `6` 
- `depends_on`: An indication that the current function depend on function function. Only relevant for composite function.  

```
functions:
  - name: warmfunction
    # This is must be set as to the same value that configured for idler on docker swarm and k8s
    # For sake of simplicity the inactivity_duration set for k8s to 5minutes
    inactivity_duration: 5
    # This param means that the number_of_requests (total) will be sent over 7 chunks.
    # For example if number_of_requests = 35000 then for each chunk we are going to send 35000/7 = 5000 requests
    # This is added in order to see the effect of the cold start time between each chunk
    chunks_number: 6
    yaml_path: functions/warm-starts-scenarios/k8s/warmfunction.yml
    environment:
      read_timeout: 5m5s
      write_timeout: 5m5s
    api:
      uri: function/warmfunction
      data: "Hello warmfunction on k8s"
      http_method: POST

```  

To start executing your experiment for nomad run the following command:
```
faas-exp run -c faas-exp/config/nomad.yaml
```