#!/bin/bash
set -e # fail and exit on error

source .env

source devscripts/common_functions.sh

printf "\nInstall pip3 requirements.txt \n\n"

pip3 install -r requirements.txt
