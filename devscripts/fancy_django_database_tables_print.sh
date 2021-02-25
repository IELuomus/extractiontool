#!/bin/bash

set -e

source .env

tables=$(mysql $DATABASE_NAME -e "show tables" | tail -n +2) 

query=""
for table in $tables;
do
    if [[ "$table" == "auth_permission" ]]; # too much info
    then 
        continue
    fi
    query="${query}select table_name from information_schema.tables where table_schema='${DATABASE_NAME}' and table_name = '${table}';"
    query="${query}select * from ${table}; "        
done

mysql $DATABASE_NAME -e "$query" > /dev/stdout

# PUIS
# mysql $DATABASE_NAME -e "show tables" > /dev/stdout

# query="\
# \! echo account_emailaddress
# select * from account_emailaddress;
# \! echo account_emailconfirmation
# select * from account_emailconfirmation;     
# \! echo auth_group
# select * from auth_group;    
# \! echo auth_group_permissions
# select * from auth_group_permissions;
# -- liikaa tietoa
# --\! echo auth_permission
# --select * from auth_permission;       
# \! echo django_admin_log
# select * from django_admin_log;   
# \! echo django_content_type
# select * from django_content_type;
# \! echo django_migrations         
# select * from django_migrations;          
# \! echo django_session
# select * from django_session;            
# \! echo django_site
# select * from django_site;               
# \! echo socialaccount_socialaccount
# select * from socialaccount_socialaccount;
# \! echo socialaccount_socialapp
# select * from socialaccount_socialapp;  
# \! echo socialaccount_socialapp_sites
# select * from socialaccount_socialapp_sites;
# \! echo socialaccount_socialtoken
# select * from socialaccount_socialtoken;
# "
# mysql ieluomus -e "$query" > /dev/stdout
