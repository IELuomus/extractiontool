#!/bin/bash

# Ubuntu 20.04

sudo apt install tesseract-ocr

sudo apt install imagemagick

# fix imagemagic

# disable this. security issue
sudo sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="none" pattern="OHTU_PROJEKTI_DISABLED_PDF" \/>/'  /etc/ImageMagick-6/policy.xml
# 1Gb to 16Gb disk memory limit. Peterson Field Guide to the Mammals_OCR.pdf fails with 1GiB.
sudo sed -i 's/<policy domain="resource" name="disk" value="1GiB"\/>/<policy domain="resource" name="disk" value="16GiB"\/>/'  /etc/ImageMagick-6/policy.xml

# relax more limits. maybe makes things faster? TODO: test speed differences.
# memory
sudo sed -i 's/<policy domain="resource" name="memory" value="256MiB"\/>/<policy domain="resource" name="memory" value="2GiB"\/>/' /etc/ImageMagick-6/policy.xml
# map
sudo sed -i 's/<policy domain="resource" name="map" value="512MiB"\/>/<policy domain="resource" name="map" value="2GiB"\/>/' /etc/ImageMagick-6/policy.xml
# width
sudo sed -i 's/<policy domain="resource" name="width" value="16KP"\/>/<policy domain="resource" name="width" value="64KP"\/>/' /etc/ImageMagick-6/policy.xml
# height
sudo sed -i 's/<policy domain="resource" name="height" value="16KP"\/>/<policy domain="resource" name="height" value="64KP"\/>/' /etc/ImageMagick-6/policy.xml
# area
sudo sed -i 's/<policy domain="resource" name="area" value="128MB"\/>/<policy domain="resource" name="area" value="2GiB"\/>/' /etc/ImageMagick-6/policy.xml
