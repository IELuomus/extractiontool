#!/bin/bash

source .env

mysql $DATABASE_NAME < devscripts/delete_document_and_dependencies_from_database.sql
