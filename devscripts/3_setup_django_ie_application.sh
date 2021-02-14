#!/bin/bash
set -e # fail and exit on error

source devscripts/common_functions.sh

echo
magenta "running: python3 manage.py makemigrations" # creates models in python(?)
python3 manage.py makemigrations

echo
magenta "running: python3 manage.py migrate" # creates database tables from models(?)
python3 manage.py migrate
