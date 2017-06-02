#!/bin/bash
RELEASE=${1:-true}

DIR=__MACOSX
echo "Deleting existing folder"
rm -rf omero_fpbioimage/static/fpbioimage/FPBioimage
if [ $RELEASE = "true" ]; then
	echo "Retrieving latest release version of FPBioimage"
	curl -s -L https://github.com/fpBioImage/fpBioImage.github.io/releases/latest | egrep -o '/fpBioImage/fpBioImage.github.io/releases/download/[v]?[0-9.]*/FPBioimage.zip' | wget --base=http://github.com/ -i - -O FPBioimage.zip
	unzip -q FPBioimage.zip
	rm FPBioimage.zip
	echo "Installing FPBioimage"
	mv FPBioimage/FPBioimage omero_fpbioimage/static/fpbioimage
	rm -rf FPBioimage
else
	echo "Retrieving FPBioimage from master"
	curl -o FPBioimage.zip -L https://github.com/fpBioImage/fpBioImage.github.io/archive/master.zip
	unzip -q FPBioimage.zip
	rm FPBioimage.zip
	mv fpBioImage.github.io-master/dev/FPBioimage omero_fpbioimage/static/fpbioimage
	rm -rf fpBioImage.github.io-master
fi

if [ -d "$DIR" ]; then
	rm -rf $DIR
fi
