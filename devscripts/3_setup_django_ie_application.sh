#!/bin/bash
set -e # fail and exit on error

source devscripts/common_functions.sh

echo "DATABASE_STATE: ${DATABASE_STATE}"
if [[ -z "${DATABASE_STATE}" ]]
then 
    # default to DROP if not set
    DATABASE_STATE='DROP'
    echo "DATABASE_STATE set to 'DROP'."
fi

if [[ "KEEP" == "$DATABASE_STATE" ]]
then
    echo "keeping database and media/* as is."
elif [[ "DROP" == "$DATABASE_STATE" ]]
then
    echo "dropping database and deleting files under 'media/*'."
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" -e "\
    DROP DATABASE IF EXISTS $DATABASE_NAME; \
    CREATE DATABASE IF NOT EXISTS $DATABASE_NAME; \
    "
    rm -rf media/*
elif [[ "DELETE" == "$DATABASE_STATE" ]]
then
    echo "deleting doc_pdf and dependent tables and deleting files under 'media/*'."
    # TODO: add dependent tables as they arrive to the database.
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" "$DATABASE_NAME" -e "\
    DELETE FROM tes_word; \
    DELETE FROM tes_line; \
    DELETE FROM tes_paragraph; \
    DELETE FROM tes_block; \
    DELETE FROM tes_page; \
    DELETE FROM doc_task; \
    DELETE FROM doc_owner; \
    DELETE FROM doc_pdf; \
    "
    rm -rf media/*
fi

echo
magenta "running: python manage.py makemigrations" # creates models in python(?)
python manage.py makemigrations

echo
magenta "running: python manage.py migrate" # creates database tables from models(?)
python manage.py migrate

echo
# komentoja jotka fiksaa jotain.
magenta "running: makemigrations, migrate, etc. commands."
set -o xtrace
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
python manage.py collectstatic --no-input --clear
set +o xtrace

# create local superusers only if database was dropped.
if [[ "DROP" == "$DATABASE_STATE" ]]
then
    echo
    magenta "creating django SUPER user:"
    magenta "   username:${DJANGO_SUPERUSER_USERNAME} password:${DJANGO_SUPERUSER_PASSWORD} email:${DJANGO_SUPERUSER_EMAIL}"
    python manage.py createsuperuser --noinput # gets values from DJANGO_SUPERUSER-variables

    echo
    magenta "updating django_site with id=1: domain:${SITE_DOMAIN} name:${SITE_NAME}"
    # CHANGE DEFAULT SITE, KEEP ID=1
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME -e "\
    UPDATE django_site SET domain='$SITE_DOMAIN', name='$SITE_NAME' WHERE id=1;
    "

    echo
    magenta "inserting into socialaccount_socialapp new line with id=1, "
    magenta "provider:${SOCIAL_PROVIDER} name:${SITE_NAME} client_id:${SOCIAL_CLIENT_ID} secret:${SOCIAL_SECRET}"
    # CHANGES
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME -e "\
    INSERT INTO socialaccount_socialapp(id, provider, name, client_id, secret, \`key\`) values(
        1,
        '$SOCIAL_PROVIDER', 
        '$SITE_NAME',
        '$SOCIAL_CLIENT_ID',
        '$SOCIAL_SECRET',
        ''
    );
    "

    echo
    magenta "inserting into socialaccount_socialapp_sites new line with id=1, sociallapp_id=1, site_id=1"
    # CHANGES
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME -e "\
    INSERT INTO socialaccount_socialapp_sites(id, socialapp_id, site_id) values(
        1,
        1,
        1
    );
    "

    echo
    magenta "add DJANGO_SUPERUSER to table account_emailaddress"
    # CHANGES
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME -e "\
    INSERT INTO account_emailaddress(id, email, verified, \`primary\`, user_id) values(
        1,
        '$DJANGO_SUPERUSER_EMAIL',
        1,
        1,
        1
    );
    "
    mysql --batch -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME -e "select * from account_emailaddress" | sed 's/\t/,/g' 2>&1

    echo
    magenta "create ANOTHER DJANGO_SUPERUSER"
    export DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME}2"
    export DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD}2"
    export DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL}2"
    magenta "   username:${DJANGO_SUPERUSER_USERNAME} password:${DJANGO_SUPERUSER_PASSWORD} email:${DJANGO_SUPERUSER_EMAIL}"
    python manage.py createsuperuser --noinput # gets values from DJANGO_SUPERUSER-variables
    echo
    magenta "add ANOTHER DJANGO_SUPERUSER to table account_emailaddress"
    # CHANGES
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME -e "\
    INSERT INTO account_emailaddress(id, email, verified, \`primary\`, user_id) values(
        2,
        '$DJANGO_SUPERUSER_EMAIL',
        1,
        1,
        2
    );
    "
    mysql --batch -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME -e "select * from account_emailaddress" | sed 's/\t/,/g' 2>&1
fi
