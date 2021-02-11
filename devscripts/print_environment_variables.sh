#!/bin/bash

printf "\neli environment variables\n\n"

function kerro {
    echo "$1: ${!1}"
}

kerro DATABASE_ROOT_PASSWORD
kerro DATABASE_HOST
kerro DATABASE_PORT
kerro DATABASE_USER
kerro DATABASE_PASSWORD
kerro DATABASE_NAME
kerro DJANGO_SECRET_KEY

# puis?
# kerro APP_CONFIG
# kerro DATABASE_SERVICE_NAME
# kerro DATABASE_ENGINE
