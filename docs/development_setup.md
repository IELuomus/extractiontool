
# IE Development Environment  

* Ubuntu only. Tested on Ubuntu 20.04, Windows 10 WSL1/Ubuntu 20.04.

## Problems
* Selain valitti jotain sertifikaatista: NET::ERR_CERT_AUTHORITY_INVALID
* Tollasta virhettä etusivun linkeistä:
```
ProgrammingError at /accounts/login/

(1146, "Table 'ieluomus.django_site' doesn't exist")
```

## Commands to Install

```
1.  cd extractiontool/

2.  cp devscripts/.env-file-example .env  

    2.1 change passwords etc. as you like in .env -file.  

3.  bash devscripts/setup_development.sh  
    * installs and sets up everything.
```

## Running the App

```
python3 manage.py runsslserver
```

## Ubuntu 20.04 Install Details

* Ubuntu packages  
    * Script will install MariaDB and Python3 and pip3 from Ubuntu packages.

* MariaDB setup
    * Database root user password will be set with $DATABASE_ROOT_PASSWORD 

    * Database $DATABASE_USER user will be created with $DATABASE_PASSWORD and all privileges.

    * Database $USER account will be created with no password and with all privileges. ( $USER = your operating system username. )

        * ( so you can use mysql command without user/password options )

    * 'ieluomus' -database will be created with $DATABASE_USER

* Python Pip3
    * requirements.txt list of packages will be installed.

