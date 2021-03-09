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

# foreign keys disabled in django-database because djano-orm performance. no much use drawing diagram without references drawn.
# create_diagram "tesseract_tables" "${DATABASE_NAME}.pdf_document|${DATABASE_NAME}.tes_.*" "Tesseract taulut"
create_diagram "pdf_tables" "${DATABASE_NAME}.pdf_.*|${DATABASE_NAME}.users_user" "Pdf taulut"
create_diagram "masterdata_tables" "${DATABASE_NAME}.masterdata_.*" "Mestaridata taulut"

echo "ls docs/database/*.png -last" 
ls docs/database/*.png -last
