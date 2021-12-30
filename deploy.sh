#!/bin/bash

# copy over the prod configuration
rm -f docker-compose.yml
cp docker-compose-prod.yml docker-compose.yml

# run Docker
DOCKER_HOST_IP=$(docker_host_ip) sudo docker-compose build --parallel || exit 1
DOCKER_HOST_IP=$(docker_host_ip) sudo docker-compose up -d
