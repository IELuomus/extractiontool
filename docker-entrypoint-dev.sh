#!/bin/sh

sleep 1

source .env
export DATABASE_HOST='db'

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
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" -h "$DATABASE_HOST" -e "\
    DROP DATABASE IF EXISTS $DATABASE_NAME; \
    CREATE DATABASE IF NOT EXISTS $DATABASE_NAME; \
    "
    rm -rf media/*
elif [[ "DELETE" == "$DATABASE_STATE" ]]
then
    echo "deleting doc_pdf and dependent tables and deleting files under 'media/*'."
    # TODO: add dependent tables as they arrive to the database.
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" "$DATABASE_NAME" -h "$DATABASE_HOST" -e "\
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

echo "running: makemigrations, migrate, etc. commands."
set -o xtrace
# for django-q
python manage.py createcachetable
python manage.py makemigrations project
python manage.py migrate project
python manage.py makemigrations users
python manage.py migrate users
python manage.py makemigrations ner_trainer
python manage.py migrate ner_trainer
python manage.py makemigrations document
python manage.py migrate document
python manage.py migrate table
python manage.py makemigrations table
python manage.py makemigrations
python manage.py migrate
set +o xtrace

echo "collect static"
python manage.py collectstatic --no-input --clear

# create local superusers only if database was dropped.
if [[ "DROP" == "$DATABASE_STATE" ]]
then
    echo
    echo "creating django SUPER user:"
    echo "   username:${DJANGO_SUPERUSER_USERNAME} password:${DJANGO_SUPERUSER_PASSWORD} email:${DJANGO_SUPERUSER_EMAIL}"
    python manage.py createsuperuser --noinput # gets values from DJANGO_SUPERUSER-variables

    echo
    echo "updating django_site with id=1: domain:${SITE_DOMAIN} name:${SITE_NAME}"
    # CHANGE DEFAULT SITE, KEEP ID=1
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME  -h "$DATABASE_HOST" -e "\
    UPDATE django_site SET domain='$SITE_DOMAIN', name='$SITE_NAME' WHERE id=1;
    "

    echo
    echo "inserting into socialaccount_socialapp new line with id=1, "
    echo "provider:${SOCIAL_PROVIDER} name:${SITE_NAME} client_id:${SOCIAL_CLIENT_ID} secret:${SOCIAL_SECRET}"
    # CHANGES
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME  -h "$DATABASE_HOST" -e "\
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
    echo "inserting into socialaccount_socialapp_sites new line with id=1, sociallapp_id=1, site_id=1"
    # CHANGES
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME  -h "$DATABASE_HOST" -e "\
    INSERT INTO socialaccount_socialapp_sites(id, socialapp_id, site_id) values(
        1,
        1,
        1
    );
    "

    echo
    echo "add DJANGO_SUPERUSER to table account_emailaddress"
    # CHANGES
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME  -h "$DATABASE_HOST" -e "\
    INSERT INTO account_emailaddress(id, email, verified, \`primary\`, user_id) values(
        1,
        '$DJANGO_SUPERUSER_EMAIL',
        1,
        1,
        1
    );
    "
    mysql --batch -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME  -h "$DATABASE_HOST" -e "select * from account_emailaddress" | sed 's/\t/,/g' 2>&1

    echo
    echo "create ANOTHER DJANGO_SUPERUSER"
    export DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME}2"
    export DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD}2"
    export DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL}2"
    echo "   username:${DJANGO_SUPERUSER_USERNAME} password:${DJANGO_SUPERUSER_PASSWORD} email:${DJANGO_SUPERUSER_EMAIL}"
    python manage.py createsuperuser --noinput # gets values from DJANGO_SUPERUSER-variables
    echo
    echo "add ANOTHER DJANGO_SUPERUSER to table account_emailaddress"
    # CHANGES
    mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME  -h "$DATABASE_HOST" -e "\
    INSERT INTO account_emailaddress(id, email, verified, \`primary\`, user_id) values(
        2,
        '$DJANGO_SUPERUSER_EMAIL',
        1,
        1,
        2
    );
    "
    mysql --batch -u $DATABASE_USER -p"$DATABASE_PASSWORD" $DATABASE_NAME  -h "$DATABASE_HOST" -e "select * from account_emailaddress" | sed 's/\t/,/g' 2>&1
fi

echo
echo "running django-q cluster in the background."
echo "python manage.py qcluster > logs/log_docker_qcluster.txt 2>&1 &" # runs django-q cluster
python -u manage.py qcluster > logs/log_docker_djangoq_cluster.txt 2>&1 &

echo
echo "running django server."
echo "python manage.py runsslserver 2>&1 | tee logs/log_django_server.txt" # runs the webserver
python -u manage.py runserver 0.0.0.0:8000 2>&1 | tee logs/log_docker_django_server.txt

# NOTE: it seems after pressing ctrl+c docker won't run anything past here but just kills the whole machine.
