#!/bin/bash

# default="\e[39m"
# red="\e[31m"
# green="\e[32m"
# blue="\e[34m"
# cyan="\e[36m"
# yellow="\e[33m"
# magenta="\e[35m"
# light_blue="\e[94m"

# https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
default="$(tput sgr 0)"
red="$(tput setaf 1)"
green="$(tput setaf 2)"
blue="$(tput setaf 4)"
lightblue="$(tput setaf 6)" # cyan
yellow="$(tput setaf 3)"
magenta="$(tput setaf 5)"

function red {
    printf "${red}$@${default}\n"
}
function green {
    printf "${green}$@${default}\n"
}
function blue {
    printf "${light_blue}$@${default}\n" # light is better
}
function yellow {
    printf "${yellow}$@${default}\n"
}
function magenta {
    printf "${magenta}$@${default}\n"
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
