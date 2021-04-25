#!/bin/sh

sleep 1

echo "migrations"
python manage.py makemigrations project
python manage.py migrate project
python manage.py makemigrations users
python manage.py migrate users
python manage.py migrate quality_control
python manage.py migrate masterdata
python manage.py migrate table
python manage.py makemigrations table
python manage.py makemigrations
python manage.py migrate

echo "collect static"
python manage.py collectstatic --no-input --clear

echo "start"
gunicorn --bind 0.0.0.0:443 --workers ${WORKER_COUNT} project.wsgi:application --certfile /certs/fullchain.pem --keyfile /certs/privkey.pem
