#!/bin/bash
set -e # fail and exit on error

# tested: Ubuntu 20.04, Windows 10 WSL1/Ubuntu 20.04, mac OS X 10.15.7, Windows 10 WSL2/Ubuntu 20.04

source devscripts/common_functions.sh

echo
case "$(get_systeemi)" in
    Linux|WSL)     
        echo "@Linux*|@WSL"
        source devscripts/ubuntu/0_install_packages.sh
        ;;
    Darwin)    
        # note: macOS
        echo "@Darwin"
        source devscripts/darwin/0_install_packages.sh
        ;;
    *)
        echo "@Something"        
        ;;
esac

source devscripts/1_setup_database.sh

source devscripts/2_setup_django.sh

source devscripts/3_setup_django_ie_application.sh

echo
green "\nAll DONE.\n"

echo
echo "to run django:"
echo "  python3 manage.py runsslserver" # runs the webserver

echo
echo "ADMIN SITE:"
blue "  https://127.0.0.1:8000/admin/"

echo
echo "NORMAL SITE:"
blue "  https://127.0.0.1:8000/"
echo
