#!/bin/bash

source tesseract_demo_functions.sh

aika_alku=$(date +%s)

export aika_alku

# loop all
find testfiles/ -name '*.pdf' -exec bash handle_pdf.sh {} \;
