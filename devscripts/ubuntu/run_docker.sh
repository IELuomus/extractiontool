#!/bin/bash

export HOST=''

# .env_docker is private copy of .env with DATABASE_HOST=db for running with docker
cp .env_docker .env

# cp docker-entrypoint.sh.local.sh docker-entrypoint.sh

sudo /etc/init.d/mysql stop

docker-compose -f docker-compose-dev.yml build 
docker-compose -f docker-compose-dev.yml up 
