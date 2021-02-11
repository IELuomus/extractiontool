#!/bin/bash

while IFS= read komento; do
    echo "$komento"
    $komento
done <<TIETOI
cat /proc/version
mariadb --version
which mariadb
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
