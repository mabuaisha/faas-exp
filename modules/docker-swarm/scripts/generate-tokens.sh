#!/bin/bash

set -e


# Extract host variables
eval "$(jq -r '@sh "MANAGER_HOST=\(.manager_host)"')"
eval "$(jq -r '@sh "BASTION_HOST=\(.bastion_host)"')"

# Get worker join token
WORKER=$(ssh -J centos@$BASTION_HOST centos@$MANAGER_HOST -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null docker swarm join-token worker -q)
MANAGER=$(ssh -J centos@$BASTION_HOST centos@$MANAGER_HOST -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null docker swarm join-token manager -q)

# Pass back a JSON object
jq -n --arg worker $WORKER --arg manager $MANAGER '{"worker":$worker,"manager":$manager}'
