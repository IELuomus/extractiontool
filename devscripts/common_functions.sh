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
