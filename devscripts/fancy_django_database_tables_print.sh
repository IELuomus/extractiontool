#!/bin/bash

mysql ieluomus -e "show tables" > /dev/stdout

query="\
\! echo EXTRACTION_TOOL_pageview
select * from EXTRACTION_TOOL_pageview;
\! echo account_emailaddress
select * from account_emailaddress;
\! echo account_emailconfirmation
select * from account_emailconfirmation;     
\! echo auth_group
select * from auth_group;    
\! echo auth_group_permissions
select * from auth_group_permissions;
-- liikaa tietoa
--\! echo auth_permission
--select * from auth_permission;       
\! echo auth_user
select * from auth_user;              
\! echo auth_user_groups
select * from auth_user_groups;
\! echo from auth_user_user_permissions
select * from auth_user_user_permissions;
\! echo django_admin_log
select * from django_admin_log;   
\! echo django_content_type
select * from django_content_type;
\! echo django_migrations         
select * from django_migrations;          
\! echo django_session
select * from django_session;            
\! echo django_site
select * from django_site;               
\! echo socialaccount_socialaccount
select * from socialaccount_socialaccount;
\! echo socialaccount_socialapp
select * from socialaccount_socialapp;  
\! echo socialaccount_socialapp_sites
select * from socialaccount_socialapp_sites;
\! echo socialaccount_socialtoken
select * from socialaccount_socialtoken;
"

mysql ieluomus -e "$query" > /dev/stdout
