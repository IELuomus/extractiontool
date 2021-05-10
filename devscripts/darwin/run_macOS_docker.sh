#!/bin/bash

# run like so:
# have .env in extractiontool/ root ( check devscripts/.env-file-example )
# bash devscripts/darwin/run_macOS_docker.sh

# docker complains if not set
export HOST=''

sudo mysql.server stop

sudo docker-compose -f docker-compose-dev.yml build 
sudo docker-compose -f docker-compose-dev.yml up 
