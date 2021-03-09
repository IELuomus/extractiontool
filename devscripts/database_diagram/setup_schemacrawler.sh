#!/bin/bash

# Ubuntu 20.04

cd devscripts/database_diagram/

tiedosto="schemacrawler-16.12.3-distribution.zip"
if [ ! -f "$tiedosto" ]; then 
    wget https://github.com/schemacrawler/SchemaCrawler/releases/download/v16.12.3/"$tiedosto"
    unzip $tiedosto
fi

sudo apt install graphviz
