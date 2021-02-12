#!/bin/bash

default="\e[39m"
red="\e[31m"
green="\e[32m"
blue="\e[34m"
cyan="\e[36m"
yellow="\e[33m"
magenta="\e[35m"
light_blue="\e[94m"

function red {
    echo -e "${red}$@${default}"
}
function green {
    echo -e "${green}$@${default}"
}
function blue {
    echo -e "${light_blue}$@${default}" # light is better
}
function yellow {
    echo -e "${yellow}$@${default}"
}
function magenta {
    echo -e "${magenta}$@${default}"
}

function get_systeemi {
    unameSystem="$(uname -s)"
    case "${unameSystem}" in
        Linux*)     
            # echo "@Linux*"
            unameSystemFull="$(uname -a)"
            if [ -z "${unameSystemFull##*Microsoft*}" ] ;then
                # echo "@Linux-WSL"
                systeemi="WSL"
                # sudo /etc/init.d/mysql restart
            else
                # echo "@Linux-Real"          
                systeemi="Linux"
            fi        
            ;;
        MSYS*)     
            # echo "@MSYS*"
            systeemi="MSYS"
            ;;
        Darwin*)    
            # echo "@MDarwin*"
            systeemi="Darwin"
            ;;
        *)  
            # echo "@Unknown"        
            systeemi="unknown"
            ;;
    esac
    echo "$systeemi"
}
