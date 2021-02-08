#!/bin/bash

function aseta_aika_alku {
    aika_alku=$(date +%s)    
    export aika_alku
}

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
function aika_nyt {
    aika_nyt=$(date +%s)
    sekunteja=$(($aika_nyt-$aika_alku))
    osa_sekunnit=$((sekunteja % 60))
    osa_minuutit=$((sekunteja / 60))
    yellow "aikaa kulunut: ${osa_minuutit}m ${osa_sekunnit}s"
}
tesseract_komento="tesseract"
dpi_resoluutio=600
function create_xml {
	filepath="$@"
	green "input image file: $filepath"
	file_dir=$(dirname "$filepath")
	file_name=$(basename "$filepath")
	blue "output xml file: output_alto/${file_dir}/${file_name}.xml"
	mkdir -p "output_alto/$file_dir"
	$tesseract_komento "output_image/$@" "output_alto/$file_dir/$file_name" -l eng --dpi "$dpi_resoluutio" alto quiet
}
function handle_pdf {
    aika_nyt
	tiedostopolku="$1"
	magenta "input pdf file: $tiedostopolku"
	tiedosto_nimi=$(basename "$tiedostopolku")	
	tiedosto_hakemisto=$(dirname "$tiedostopolku")
	# echo "filepath_basename: ${tiedosto_nimi}"
	# echo "filepath_dirname: $tiedosto_hakemisto"
	
	full_image_output_path="output_image/$tiedostopolku"

    # esim: output image filepath: output_image/testfiles/Anderson_et_al-1985-Journal_of_Zoology.pdf/
	green "output image filepath: ${full_image_output_path}/"

	mkdir -p "$full_image_output_path"
    sivuja=$(qpdf --show-npages "$tiedosto_hakemisto/$tiedosto_nimi")
    for (( i=0 ; i<sivuja ; i++ ))
    do
        green "output image: ${full_image_output_path}/${tiedosto_nimi}-${i}.png"
        convert -density "$dpi_resoluutio" "${tiedosto_hakemisto}/${tiedosto_nimi}"[$i] "${full_image_output_path}/${tiedosto_nimi}-${i}.png"
    done

    echo "("$(aika_nyt)")"
	# loop created images
	image_output_path="$tiedostopolku" # withouth output_image
	while IFS=: read image_file_name
	do
		# echo "creating path (if not exists): $image_output_path"
		create_xml "$image_output_path/$image_file_name"
	done < <(cd "$full_image_output_path/" && ls -1 --time=ctime | tac)
}
