#!/bin/bash

TAG=v2.1.1
DIR=__MACOSX
echo "Retrieving FPBioimage"
curl -o FPBioimage.zip -L https://github.com/fpBioImage/fpBioImage.github.io/releases/download/$TAG/FPBioimage.zip
unzip -q FPBioimage.zip
rm FPBioimage.zip
# clean if we want to replace version
echo "Installing FPBioimage"
rm -rf omero_fpbioimage/static/fpbioimage/FPBioimage
mv FPBioimage/FPBioimage omero_fpbioimage/static/fpbioimage
rm -rf FPBioimage
if [ -d "$DIR" ]; then
	rm -rf $DIR
fi
