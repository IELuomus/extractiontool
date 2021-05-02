#!/bin/bash
set -e # fail and exit on error

run_server=$1

# tested: Ubuntu 20.04, Windows 10 WSL1/Ubuntu 20.04, mac OS X 10.15.7, Windows 10 WSL2/Ubuntu 20.04

source devscripts/common_functions.sh

# ignore installing packages if given argument 'fast' (bash devscripts/setup_development.sh fast)
if [[ "$1" == "fast" ]] ;
then
    echo "FAST: skip installing system packages."
else
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
fi

source devscripts/1_setup_database.sh

# ignore installing packages if given argument 'fast' (bash devscripts/setup_development.sh fast)
if [[ "$1" == "fast" ]] ;
then
    echo "FAST: skip installing django packages."
else
    source devscripts/2_setup_django.sh
fi

source devscripts/3_setup_django_ie_application.sh

echo
green "\nSETUP All DONE.\n"

echo
echo "ADMIN SITE:"
blue "  https://127.0.0.1:8000/admin/"

echo
echo "NORMAL SITE:"
blue "  https://127.0.0.1:8000/"
echo

if [[ "$run_server" == "yes" ]]
then
    bash devscripts/run_server.sh
fi



green "SCRIPT END."
