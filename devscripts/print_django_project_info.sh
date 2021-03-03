#!/bin/bash

function aja {
    printf "\nRUNNING COMMAND: $@\n\n"
    $@
}

aja "python3 manage.py diffsettings"

aja "python3 manage.py inspectdb"

aja "python3 manage.py showmigrations"

# TODO: maybe add something?