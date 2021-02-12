#!/bin/bash
set -e # fail and exit on error

# testattu: Ubuntu 20.04, Windows 10 WSL1/Ubuntu 20.04

source devscripts/ubuntu/0_install_packages.sh

source devscripts/ubuntu/1_setup_database.sh

source devscripts/ubuntu/2_setup_django.sh

source devscripts/ubuntu/3_setup_django_ie_application.sh

green "\nAll DONE. $(blue 'to run django:\n')"
magenta "python3 manage.py runsslserver" # runs the webserver
echo
