#!/bin/bash

source devscripts/common_functions.sh

function aja {
    echo "$@"
    $@
}

case "$(get_systeemi)" in
    Linux|WSL)     
        echo "@Linux*|@WSL"
        aja "cat /proc/version"
        ;;
    Darwin)    
        echo "@Darwin"
        aja "sw_vers"
        ;;
    *)
        echo "@Something"        
        ;;
esac

while IFS= read komento; do
    echo "$komento"
    $komento
done <<TIETOI
mariadb --version
which mariadb
mysql --version
which mysql
pip3 --version
which pip3
python3 --version
which python3
ls -l $(which python3)
TIETOI
