#!/bin/bash

# Ubuntu 20.04

set -e

bash devscripts/database_diagram/setup_schemacrawler.sh

# run this in extractiontool/ with bash docs/database/create_diagrams.sh

alku=$(pwd)

set -a
source .env
set +a

echo "env | grep DATABASE"
env | grep DATABASE

function create_diagram {
    filename_prefix="$1"
    output_file="${filename_prefix}.png"
    tables="$2"
    title="$3"

    echo "tables: $tables"

    cd devscripts/database_diagram/schemacrawler-16.12.3-distribution/_schemacrawler/
    bash schemacrawler.sh --title="${title}" --tables="$tables" --command="schema" --output-format="png" --output-file="${output_file}" --info-level=standard --url="jdbc:mysql://localhost:3306/${DATABASE_NAME}?user=${DATABASE_USER}&password=${DATABASE_PASSWORD}"
    cp "$output_file" "${alku}/docs/database/"
    cd "$alku"
}

create_diagram "document_tables" "${DATABASE_NAME}.doc_.*|${DATABASE_NAME}.users_user" "Document tables"
create_diagram "ieluomus_tables" "${DATABASE_NAME}.doc_pdf|${DATABASE_NAME}.project_traittable|${DATABASE_NAME}.ner_trainer_traitnamelearndata|${DATABASE_NAME}.table_json_table" "IELuomus tables"
create_diagram "tesseract_tables" "${DATABASE_NAME}.doc_pdf|${DATABASE_NAME}.tes_.*" "Tesseract tables"
create_diagram "djangoq_tables" "${DATABASE_NAME}.ieluomus_djangoq_cache_table|${DATABASE_NAME}.django_q_.*" "Django-q tables"
create_diagram "django_tables" "${DATABASE_NAME}.django_[^q].*|${DATABASE_NAME}.socialaccount_.*|${DATABASE_NAME}.auth_.*|${DATABASE_NAME}.account_.*|${DATABASE_NAME}.users_.*" "Django native tables"

echo "ls docs/database/*.png -last" 
ls docs/database/*.png -last
