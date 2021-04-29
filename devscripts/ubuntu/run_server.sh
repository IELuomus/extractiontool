#!/bin/bash

# .env_dev is private copy of .env for running local server
cp .env_dev .env

sudo /etc/init.d/mysql start

python manage.py runsslserver
