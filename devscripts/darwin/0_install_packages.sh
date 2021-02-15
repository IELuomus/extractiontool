#!/bin/bash
set -e # fail and exit on error

printf "\nupdate package-list and install MariaDB and Python3\n\n"

printf "running brew update\n"
brew update --verbose # yes?
 
# install mariadb and stuff
brew install mariadb
# install python3 and pip3 and stuff
brew install python3

# configure mariadb to start automagically
brew services start mariadb
