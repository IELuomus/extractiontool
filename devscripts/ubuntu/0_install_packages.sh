#!/bin/bash
set -e # fail and exit on error

printf "\nupdate package-list and install MariaDB and Python3\n\n"

sudo apt-get update # yes
 
# install mariadb and stuff
sudo apt install mariadb-server
 
# WSL 20.04
# The following additional packages will be installed:
#   galera-3 libcgi-fast-perl libcgi-pm-perl libconfig-inifiles-perl libdbd-mysql-perl libdbi-perl libfcgi-perl libhtml-template-perl libmysqlclient21 libterm-readkey-perl
#   mariadb-client-10.3 mariadb-client-core-10.3 mariadb-common mariadb-server-10.3 mariadb-server-core-10.3 mysql-common socat
# Suggested packages:
#   libmldbm-perl libnet-daemon-perl libsql-statement-perl libipc-sharedcache-perl mailx mariadb-test tinyca
# The following NEW packages will be installed:
#   galera-3 libcgi-fast-perl libcgi-pm-perl libconfig-inifiles-perl libdbd-mysql-perl libdbi-perl libfcgi-perl libhtml-template-perl libmysqlclient21 libterm-readkey-perl
#   mariadb-client-10.3 mariadb-client-core-10.3 mariadb-common mariadb-server mariadb-server-10.3 mariadb-server-core-10.3 mysql-common socat
# 0 upgraded, 18 newly installed, 0 to remove and 21 not upgraded.
# Real Ubuntu 20.04
# The following additional packages will be installed:
#   galera-3 gawk libaio1 libcgi-fast-perl libcgi-pm-perl libconfig-inifiles-perl libdbd-mysql-perl libdbi-perl libfcgi-perl libhtml-template-perl libreadline5
#   libterm-readkey-perl mariadb-client-10.3 mariadb-client-core-10.3 mariadb-common mariadb-server-10.3 mariadb-server-core-10.3
# Suggested packages:
#   gawk-doc libmldbm-perl libnet-daemon-perl libsql-statement-perl libipc-sharedcache-perl mailx mariadb-test tinyca
# The following NEW packages will be installed:
#   galera-3 gawk libaio1 libcgi-fast-perl libcgi-pm-perl libconfig-inifiles-perl libdbd-mysql-perl libdbi-perl libfcgi-perl libhtml-template-perl libreadline5
#   libterm-readkey-perl mariadb-client-10.3 mariadb-client-core-10.3 mariadb-common mariadb-server mariadb-server-10.3 mariadb-server-core-10.3
# 0 upgraded, 18 newly installed, 0 to remove and 0 not upgraded.

sudo apt-get install libmariadb3
sudo apt-get install libmariadb-dev

# install python3 and pip3 and stuff
sudo apt install python3 python3-pip

# Real Ubuntu 20.04
# The following additional packages will be installed:
#   libexpat1-dev libpython3-dev libpython3.8-dev python-pip-whl python3-dev python3-distutils python3-lib2to3 python3-setuptools python3-wheel python3.8-dev zlib1g-dev
# Suggested packages:
#   python-setuptools-doc
# The following NEW packages will be installed:
#   libexpat1-dev libpython3-dev libpython3.8-dev python-pip-whl python3-dev python3-distutils python3-lib2to3 python3-pip python3-setuptools python3-wheel python3.8-dev zlib1g-dev
# 0 upgraded, 12 newly installed, 0 to remove and 0 not upgraded.

