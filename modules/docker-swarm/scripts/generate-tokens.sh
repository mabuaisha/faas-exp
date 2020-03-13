#!/bin/bash

set -e

# Extract required host variables
eval "$(jq -r '@sh "export BASTION_HOST=\(.bastion_host) MANAGER_HOST=\(.manager_host)"')"

# Extract required host worker & manager tokens
WORKER=$(ssh -o ProxyCommand="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -W %h:%p centos@${BASTION_HOST}" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null centos@${MANAGER_HOST} "docker swarm join-token worker -q")
MANAGER=$(ssh -o ProxyCommand="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -W %h:%p centos@${BASTION_HOST}" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null centos@${MANAGER_HOST} "docker swarm join-token manager -q")

# Pass back a JSON object
jq -n --arg worker $WORKER --arg manager $MANAGER '{"worker":$worker,"manager":$manager}'
