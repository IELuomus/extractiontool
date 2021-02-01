#!/bin/bash

# TODO

komento="tesseract"

function tessa {
	echo "file: $@"
	output_file=$(basename "$@")
	echo "output_file: $output_file"
	$komento "$@" "output/$output_file" -l eng alto
}
#export -f tessa

# loop all
#find testfiles/ -name '*.pdf' -exec bash -c 'tessa "$0"' {} \;



