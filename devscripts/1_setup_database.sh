#!/bin/bash
set -e # fail and exit on error

source .env

source devscripts/print_environment_variables.sh

source devscripts/common_functions.sh

# restarting MariaDB seems to be needed sometimes
echo
systeemi=$(get_systeemi)
case "${systeemi}" in
    Linux)     
        echo "@Linux*"
        sudo /etc/init.d/mysql restart    
        ;;
    WSL)
        echo "@WSL"
        sudo /etc/init.d/mysql restart    
        ;;
    Darwin)    
        echo "@Darwin"
        sudo mysql.server start
        ;;
    *)
        echo "@Something"        
        ;;
esac

komento="mysql" # /usr/bin/mysql

root_komento="sudo $komento -u root "

printf "\nMariaDB\n\n"

$root_komento<<LAUSE
FLUSH TABLES;
FLUSH PRIVILEGES;
\! echo @creating new database user \'$USER@localhost\'
CREATE USER IF NOT EXISTS '$USER'@'localhost';
\! echo @creating new database user \'$DATABASE_USER@localhost\'
CREATE USER IF NOT EXISTS '$DATABASE_USER'@'localhost';
FLUSH TABLES;
FLUSH PRIVILEGES;
\! echo @setting \'$USER\' password to empty string
ALTER USER '$USER'@'localhost' IDENTIFIED by '';
\! echo @granting privileges to \'$USER@localhost\'
GRANT ALL PRIVILEGES ON *.* TO '$USER'@'localhost';
\! echo @setting \'$DATABASE_USER\' password to \'$DATABASE_PASSWORD\'
ALTER USER '$DATABASE_USER'@'localhost' IDENTIFIED by '$DATABASE_PASSWORD';
\! echo @granting privileges to \'$DATABASE_USER@localhost\'
GRANT ALL PRIVILEGES ON *.* TO '$DATABASE_USER'@'localhost';
LAUSE
