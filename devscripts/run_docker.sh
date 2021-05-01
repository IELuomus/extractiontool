#!/bin/bash

mkdir -p logs/

# docker complains if not set
export HOST=''

sudo /etc/init.d/mysql stop

sudo docker-compose -f docker-compose-dev.yml build 
sudo docker-compose -f docker-compose-dev.yml up 
