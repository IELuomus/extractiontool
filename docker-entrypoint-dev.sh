#!/bin/sh

sleep 1

echo "migrations"
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
python manage.py 
# for django-q
python manage.py createcachetable

echo "collect static"
python manage.py collectstatic --no-input --clear

source .env

echo
echo "creating django SUPER user:"
echo "   username:${DJANGO_SUPERUSER_USERNAME} password:${DJANGO_SUPERUSER_PASSWORD} email:${DJANGO_SUPERUSER_EMAIL}"
python3 manage.py createsuperuser --noinput # gets values from DJANGO_SUPERUSER-variables

echo
echo "updating django_site with id=1: domain:${SITE_DOMAIN} name:${SITE_NAME}"
# CHANGE DEFAULT SITE, KEEP ID=1

mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" -h "$DATABASE_HOST" $DATABASE_NAME<<LAUSE
UPDATE django_site SET domain="$SITE_DOMAIN", name="$SITE_NAME" WHERE id=1;
LAUSE

echo
echo "inserting into socialaccount_socialapp new line with id=1, "
echo "provider:${SOCIAL_PROVIDER} name:${SITE_NAME} client_id:${SOCIAL_CLIENT_ID} secret:${SOCIAL_SECRET}"
# CHANGES
mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" -h "$DATABASE_HOST" $DATABASE_NAME<<LAUSE
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
echo "inserting into socialaccount_socialapp_sites new line with id=1, sociallapp_id=1, site_id=1"
# CHANGES
mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" -h "$DATABASE_HOST" $DATABASE_NAME<<LAUSE
INSERT INTO socialaccount_socialapp_sites(id, socialapp_id, site_id) values(
    1,
    1,
    1
);
LAUSE

echo
echo "add DJANGO_SUPERUSER to table account_emailaddress"
# CHANGES
mysql -u $DATABASE_USER -p"$DATABASE_PASSWORD" -h "$DATABASE_HOST" $DATABASE_NAME<<LAUSE
INSERT INTO account_emailaddress(id, email, verified, \`primary\`, user_id) values(
    1,
    "$DJANGO_SUPERUSER_EMAIL",
    1,
    1,
    1
);
LAUSE
mysql --batch -u $DATABASE_USER -p"$DATABASE_PASSWORD" -h "$DATABASE_HOST" $DATABASE_NAME -e "select * from account_emailaddress" | sed 's/\t/,/g' 2>&1

echo "stard django-q background service"
python manage.py qcluster &
sleep 5 # let it start 

echo "start django server"
python manage.py runserver 0.0.0.0:8000
