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
# for django-q
python manage.py createcachetable

echo "collect static"
python manage.py collectstatic --no-input --clear

echo "stard django-q background service"
python manage.py qcluster > log_docker_djangoq_prod.txt 2>&1 &

echo "start"
gunicorn --bind 0.0.0.0:443 --workers ${WORKER_COUNT} project.wsgi:application --certfile /certs/fullchain.pem --keyfile /certs/privkey.pem
