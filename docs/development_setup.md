
# IE Development Environment  


## Setup Development Environment

```
1.  cd extractiontool/

2.  cp devscripts/.env-file-example .env  
    * change passwords etc. as you like in .env -file.  

3.  bash devscripts/setup_development.sh  
    * installs and sets up everything.
```

* Tested on
    * Ubuntu 20.04, Windows 10 WSL1/Ubuntu 20.04., Windows 10 WSL2/Ubuntu20.04
    * Apple mac OS X 10.15.7

### Problems
* Selain valitti jotain sertifikaatista: NET::ERR_CERT_AUTHORITY_INVALID

### Install Details

* Ubuntu/Brew packages
    * Script will install MariaDB and Python3 and pip3 from package repository.

* MariaDB setup
    * ~~Database root user password will be set with $DATABASE_ROOT_PASSWORD~~  
        * disabled for now.

    * Database $DATABASE_USER user will be created with $DATABASE_PASSWORD and all privileges.

    * Database $USER account will be created with no password and with all privileges. ( $USER = your operating system username. )

        * ( so you can use mysql command without user/password options )

    * 'ieluomus' -database will be created with $DATABASE_USER

* Python Pip3
    * requirements.txt list of packages will be installed.  

* Djanjo application
    * Script to create models for our application is run.
    * Database tables from the models are created for our application in our database.
    * Various migration commands and collectstatic command is run.
    * django SuperUser is created with $DJANGO_SUPERUSER_PASSWORD, $DJANGO_SUPERUSER_USERNAME, $DJANGO_SUPERUSER_EMAIL.
    * Some database tables are updated to skip creating social media site manually.
        * UPDATE django_site SET domain="$SITE_DOMAIN", name="$SITE_NAME" WHERE id=1;
        * INSERT INTO socialaccount_socialapp(id, provider, name, client_id, secret, \`key\`) values(1,"$SOCIAL_PROVIDER", "$SITE_NAME", "$SOCIAL_CLIENT_ID","$SOCIAL_SECRET","");  
        * INSERT INTO socialaccount_socialapp_sites(id, socialapp_id, site_id) values(1,1,1);
    * Database is updated to skip verification email for superuser.
        * INSERT INTO account_emailaddress(id, email, verified, \`primary\`, user_id) values(1,"$DJANGO_SUPERUSER_EMAIL",1,1,1);

## Running the App

```
python3 manage.py runsslserver
```

## Other Scripts
```
bash devscripts/print_environment_variadbes.sh
```
* prints current shell IE project environment variables.
* used by other scripts to print variables.
* not really useful locally if .env file is used.

```
bash devscripts/print_environment_system.sh
```
* prints mariadb, python versions.

```
bash devscripts/print_django_project_info.sh
```
* prints some django project info.
    