#!/bin/bash
set -e # fail and exit on error

printf "\nupdate package-list and install MariaDB and Python3\n\n"

sudo apt-get update # yes
 
# install mariadb and stuff
sudo apt install mariadb-server

# new unteouched Ubuntu 20.04 install in WSL2 :
# Reading state information... Done
# The following additional packages will be installed:
#   galera-3 libcgi-fast-perl libcgi-pm-perl libconfig-inifiles-perl libdbd-mysql-perl libdbi-perl libencode-locale-perl libfcgi-perl libhtml-parser-perl libhtml-tagset-perl libhtml-template-perl libhttp-date-perl libhttp-message-perl
#   libio-html-perl liblwp-mediatypes-perl libmysqlclient21 libsnappy1v5 libterm-readkey-perl libtimedate-perl liburi-perl mariadb-client-10.3 mariadb-client-core-10.3 mariadb-common mariadb-server-10.3 mariadb-server-core-10.3
#   mysql-common socat
# Suggested packages:
#   libclone-perl libmldbm-perl libnet-daemon-perl libsql-statement-perl libdata-dump-perl libipc-sharedcache-perl libwww-perl mailx mariadb-test tinyca
# The following NEW packages will be installed:
#   galera-3 libcgi-fast-perl libcgi-pm-perl libconfig-inifiles-perl libdbd-mysql-perl libdbi-perl libencode-locale-perl libfcgi-perl libhtml-parser-perl libhtml-tagset-perl libhtml-template-perl libhttp-date-perl libhttp-message-perl
#   libio-html-perl liblwp-mediatypes-perl libmysqlclient21 libsnappy1v5 libterm-readkey-perl libtimedate-perl liburi-perl mariadb-client-10.3 mariadb-client-core-10.3 mariadb-common mariadb-server mariadb-server-10.3
#   mariadb-server-core-10.3 mysql-common socat

# needed for python mysqlclient 
sudo apt-get install libmariadb3
sudo apt-get install libmariadb-dev
# install python3 and pip3 and stuff
sudo apt install python3 python3-pip

sudo apt install imagemagick
sudo apt install tesseract-ocr
sudo apt install ghostscript-x

# disable this. this is security issue enabled which prevents doing anything..
sudo sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="none" pattern="OHTU_PROJEKTI_DISABLED_PDF" \/>/'  "/etc/ImageMagick-6/policy.xml"
