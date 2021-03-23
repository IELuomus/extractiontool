#!/bin/sh

sleep 1

echo "migrations"
python manage.py makemigrations project
python manage.py migrate project
python manage.py makemigrations users
python manage.py migrate users
python manage.py migrate quality_control
python manage.py migrate masterdata
python manage.py makemigrations
python manage.py migrate

echo "collect static"
python manage.py collectstatic --no-input --clear

echo "start"
python manage.py runsslserver 0.0.0.0:8000