#!/bin/bash

mkdir -p logs/

source devscripts/common_functions.sh

echo
cyan "RUNNING SERVER AND DJANGO-Q."
echo

cyan "starting mysql server (if not started)."
sudo /etc/init.d/mysql start

echo
cyan "running django-q cluster in the background."
echo "python manage.py qcluster > log_qcluster.txt 2>&1 &" # runs django-q cluster
python manage.py qcluster > logs/log_djangoq_cluster.txt 2>&1 &
task_id_djangoq_cluster=$!

echo
cyan "running django server."
echo "python manage.py runsslserver 2>&1 | tee log_django_server.txt" # runs the webserver
python manage.py runsslserver 2>&1 | tee logs/log_django_server.txt
echo "django server stopped."

echo
cyan "stopping django-q cluster."
echo "kill $task_id_djangoq_cluster"
kill $task_id_djangoq_cluster
echo "django-q cluster stopped."
