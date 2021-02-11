#!/bin/bash
set -e # fail and exit on error

# testattu: Ubuntu 20.04

source devscripts/ubuntu/0_install_packages.sh

source devscripts/ubuntu/1_setup_database.sh

source devscripts/ubuntu/2_setup_django.sh

green "\nAll DONE. $(blue 'to run django:\n')"
magenta "python3 manage.py runsslserver"
echo
