#!/bin/bash

printf "\neli environment variables\n\n"

# note: this is used in other scripts
# only useful in commandline if variables are set.
# could load them, but what's the point?:
#   set allexport -o
#   source my_env_file_x.env
#   set allexport +o

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
