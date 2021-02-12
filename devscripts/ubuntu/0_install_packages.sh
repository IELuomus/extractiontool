#!/bin/bash
set -e # fail and exit on error

printf "\nupdate package-list and install MariaDB and Python3\n\n"

sudo apt-get update # yes
 
# install mariadb and stuff
sudo apt install mariadb-server
# needed for python mysqlclient 
sudo apt-get install libmariadb3
sudo apt-get install libmariadb-dev
# install python3 and pip3 and stuff
sudo apt install python3 python3-pip
