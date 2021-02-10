#!/bin/bash

source tesseract_demo_functions.sh

file1='testfiles/1305599480.pdf' # text-pdf
file2='testfiles/Books/Peterson Field Guide to the Mammals_OCR.pdf' # ocr-converted-pdf
file3='testfiles/39 Geiser 2009.pdf' # small

aseta_aika_alku

handle_pdf "$file1" # works
# handle_pdf "$file2" # hidas
handle_pdf "$file3" # works, small and fast
