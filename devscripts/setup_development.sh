#!/bin/bash
set -e # fail and exit on error

# tested: Ubuntu 20.04, Windows 10 WSL1/Ubuntu 20.04, mac OS X 10.15.7

source devscripts/common_functions.sh

echo
case "$(get_systeemi)" in
    Linux|WSL)     
        echo "@Linux*|@WSL"
        source devscripts/ubuntu/0_install_packages.sh
        ;;
    Darwin)    
        # note: macOS UI design is crap
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

green "\nAll DONE. $(blue 'to run django:\n')"
magenta "python3 manage.py runsslserver" # runs the webserver
echo
