#!/bin/bash

DIR=__MACOSX
echo "Retrieving latest FPBioimage"
curl -s -L https://github.com/fpBioImage/fpBioImage.github.io/releases/latest | egrep -o '/fpBioImage/fpBioImage.github.io/releases/download/[v]?[0-9.]*/FPBioimage.zip' | wget --base=http://github.com/ -i - -O FPBioimage.zip
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
