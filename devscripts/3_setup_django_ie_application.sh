#!/bin/bash
set -e # fail and exit on error

source devscripts/common_functions.sh

echo
magenta "running: python3 manage.py makemigrations" # creates models in python(?)
python3 manage.py makemigrations

echo
magenta "running: python3 manage.py migrate" # creates database tables from models(?)
python3 manage.py migrate

echo
# komentoja jotka fiksaa jotain.
magenta "running: komentoja jotka fiksaa jotain"
cat<<KOMENTOJA 
python manage.py makemigrations project
python manage.py migrate project
python manage.py makemigrations users
python manage.py migrate users
python manage.py migrate ner_trainer
python manage.py makemigrations table
python manage.py migrate table
python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable
python manage.py collectstatic
KOMENTOJA

python3 manage.py makemigrations project
python3 manage.py migrate project
python3 manage.py makemigrations users
python3 manage.py migrate users
python3 manage.py migrate ner_trainer
python manage.py makemigrations table
python3 manage.py migrate table
python3 manage.py makemigrations
python3 manage.py migrate
python manage.py createcachetable
python3 manage.py collectstatic<<JEP
yes
JEP

echo
magenta "creating django SUPER user:"
magenta "   username:${DJANGO_SUPERUSER_USERNAME} password:${DJANGO_SUPERUSER_PASSWORD} email:${DJANGO_SUPERUSER_EMAIL}"
python3 manage.py createsuperuser --noinput # gets values from DJANGO_SUPERUSER-variables

echo
magenta "updating django_site with id=1: domain:${SITE_DOMAIN} name:${SITE_NAME}"
# CHANGE DEFAULT SITE, KEEP ID=1
mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME<<LAUSE
UPDATE django_site SET domain="$SITE_DOMAIN", name="$SITE_NAME" WHERE id=1;
LAUSE

echo
magenta "inserting into socialaccount_socialapp new line with id=1, "
magenta "provider:${SOCIAL_PROVIDER} name:${SITE_NAME} client_id:${SOCIAL_CLIENT_ID} secret:${SOCIAL_SECRET}"
# CHANGES
mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME<<LAUSE
INSERT INTO socialaccount_socialapp(id, provider, name, client_id, secret, \`key\`) values(
    1,
    "$SOCIAL_PROVIDER", 
    "$SITE_NAME",
    "$SOCIAL_CLIENT_ID",
    "$SOCIAL_SECRET",
    ""
);
LAUSE

echo
magenta "inserting into socialaccount_socialapp_sites new line with id=1, sociallapp_id=1, site_id=1"
# CHANGES
mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME<<LAUSE
INSERT INTO socialaccount_socialapp_sites(id, socialapp_id, site_id) values(
    1,
    1,
    1
);
LAUSE

# select * from socialaccount_socialaccount; select * from socialaccount_socialapp;select * from socialaccount_socialapp_sites;select * from socialaccount_socialtoken;
# select * from socialaccount_socialaccount; 
# select * from socialaccount_socialapp;
# select * from socialaccount_socialapp_sites;
# select * from socialaccount_socialtoken;

echo
magenta "add DJANGO_SUPERUSER to table account_emailaddress"
# CHANGES
mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME<<LAUSE
INSERT INTO account_emailaddress(id, email, verified, \`primary\`, user_id) values(
    1,
    "$DJANGO_SUPERUSER_EMAIL",
    1,
    1,
    1
);
LAUSE
mysql --batch -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME -e "select * from account_emailaddress" | sed 's/\t/,/g' 2>&1


