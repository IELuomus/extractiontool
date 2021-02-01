#!/bin/bash

tesseract_komento="tesseract"
dpi_resoluutio=300

function create_xml {
	echo "file: $@"
	output_file=$(basename "$@")
	echo "output_file: $output_file"
	$tesseract_komento "$@" "output_alto/$output_file" -l eng --dpi "$dpi_resoluutio" alto
}

# text-pdf
file1='1305599480.pdf'
# ocr-converted-pdf
file2='Books/Peterson Field Guide to the Mammals_OCR.pdf'

function handle_pdf {
	filename="$1"
	image_output_path="output_image/$filename"
	echo "pdf-filename:${filename}"
	mkdir -p "$image_output_path"
	convert -trim -density "$dpi_resoluutio" -quality 100 "testfiles/$filename" "$image_output_path/$filename.png"
	# loop created images
	while IFS=: read image_file_name
	do
		echo "$image_file_name"
		create_xml "$image_output_path/$image_file_name"
	done < <(cd "$image_output_path/" && ls -1 --time=ctime | tac)
}

handle_pdf "$file1"
#handle_pdf "$file2" # jää jumiin.
