#!/bin/bash

# following this guide https://docs.docker.com/engine/install/ubuntu/
# and this https://docs.docker.com/compose/install/

# tested on Ubuntu 20.04

# remove possible old version
echo "@remove old"
sudo apt-get remove docker docker-engine docker.io containerd runc

# set up repository
echo '@set up repository'
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
## set up 'stable' repository
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# install docker engine
echo "@install docker engine"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
## list versions
apt-cache madison docker-ce
## set version to get
VERSION_STRING='5:20.10.6~3-0~ubuntu-focal'
## get it
sudo apt-get install docker-ce="${VERSION_STRING}" docker-ce-cli="${VERSION_STRING}" containerd.io

# run hello world
echo "@run hello world"
sudo docker run hello-world

# install docker compose also..
echo "install docker-compose"
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

echo "@script end"
