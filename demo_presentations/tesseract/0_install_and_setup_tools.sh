#!/bin/bash

# Ubuntu 20.04

sudo apt install tesseract-ocr

sudo apt install imagemagick

sudo apt install qpdf

# fix ImageMagick
tiedosto="/etc/ImageMagick-6/policy.xml"

# disable this. this is security issue enabled which prevents doing anything..
sudo sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="none" pattern="OHTU_PROJEKTI_DISABLED_PDF" \/>/'  "$tiedosto"
# 1Gb to 16Gb disk memory limit. Peterson Field Guide to the Mammals_OCR.pdf fails with 1GiB.
sudo sed -i 's/<policy domain="resource" name="disk" value="1GiB"\/>/<policy domain="resource" name="disk" value="16GiB"\/>/'  "$tiedosto"

# relax more limits.
# imagemagick really likes memory. with 8GiB about 4 times faster than 2GiB.
# e.g. convert 5-1-PB.pdf used 7GiB memory in Windows Task Manager, script running on WSL/Ubuntu 20.04
# Books/Gardner_Mammals of South America Vol 1-Marsupials Xenarthrans Shrews and Bats.pdf used 8.2GiB
MB_LIMIT="16GiB" # 16GiB = ~60x times more memory..
KB_LIMIT="256KP"

sudo sed -i 's/<policy domain="resource" name="memory" value="256MiB"\/>/<policy domain="resource" name="memory" value="'$MB_LIMIT'"\/>/' "$tiedosto"   # memory
sudo sed -i 's/<policy domain="resource" name="map" value="512MiB"\/>/<policy domain="resource" name="map" value="'$MB_LIMIT'"\/>/' "$tiedosto" # map
sudo sed -i 's/<policy domain="resource" name="width" value="16KP"\/>/<policy domain="resource" name="width" value="'$KB_LIMIT'"\/>/' "$tiedosto"   # width
sudo sed -i 's/<policy domain="resource" name="height" value="16KP"\/>/<policy domain="resource" name="height" value="'$KB_LIMIT'"\/>/' "$tiedosto" # height
sudo sed -i 's/<policy domain="resource" name="area" value="128MB"\/>/<policy domain="resource" name="area" value="'$MB_LIMIT'"\/>/' "$tiedosto"    # area

echo "$tiedosto"

# alkup.

# pakolliset
# <policy domain="coder" rights="none" pattern="PDF" />
# <policy domain="resource" name="disk" value="1GiB"/>

# performance-säätö-testit
# <policy domain="resource" name="memory" value="256MiB"/>
# <policy domain="resource" name="map" value="512MiB"/>
# <policy domain="resource" name="width" value="16KP"/>
# <policy domain="resource" name="height" value="16KP"/>
# <policy domain="resource" name="area" value="128MB"/>