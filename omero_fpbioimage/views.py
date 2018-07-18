#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (c) 2017 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# FPBioimage was originally published in
# <https://www.nature.com/nphoton/journal/v11/n2/full/nphoton.2016.273.html>.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Version: 1.0
#

from django.http import HttpResponse
from django.shortcuts import render
from omeroweb.webclient.decorators import login_required

import numpy as np
import math
import PIL
from PIL import Image
from cStringIO import StringIO


def index(request):

    return HttpResponse("FPBioimage Index")


@login_required()
def fpbioimage(request, image_id, conn=None, **kwargs):
    """Load the viewer page for the image."""
    image = conn.getObject('Image', image_id)
    px = image.getPrimaryPixels().getPhysicalSizeX()
    x = 1
    y = 1
    z = 1

    if px is not None:
        size = image.getPixelSizeX(True)
        x = size.getValue()

    py = image.getPrimaryPixels().getPhysicalSizeY()
    if py is not None:
        size = image.getPixelSizeY(True)
        y = size.getValue()

    pz = image.getPrimaryPixels().getPhysicalSizeZ()
    if pz is not None:
        size = image.getPixelSizeZ(True)
        z = size.getValue()

    context = {'image': image,
               'size_x': x,
               'size_y': y,
               'size_z': z
               }
    return render(request, 'fpbioimage/viewer.html', context)


def ceil2(x):
    print "ceil", x, type(x)
    # Round up to the next power of 2
    return 1<<(x-1).bit_length()


@login_required()
def fpbioimage_png(request, image_id, atlas_index, conn=None, **kwargs):
    """Render png for image at specified Z section."""
    image = conn.getObject('image', image_id)

    # TODO: If > 512 * 512 need to scale down
    sliceWidth = image.getSizeX()
    sliceHeight = image.getSizeY()
    numSlices = image.getSizeZ()

    numberOfAtlases = 8 # Set for FPBioimage v4

    # Calculate necessary variables
    paddedSliceWidth = ceil2(sliceWidth)
    paddedSliceHeight = ceil2(sliceHeight)

    xOffset = math.floor((paddedSliceWidth-sliceWidth)/2)
    yOffset = math.floor((paddedSliceHeight-sliceHeight)/2)

    slicesPerAtlas = math.ceil(numSlices/numberOfAtlases)
    atlasWidth = ceil2(paddedSliceWidth)
    atlasHeight = ceil2(int(paddedSliceHeight * slicesPerAtlas))
    while (atlasHeight > 2*atlasWidth) & (atlasHeight > sliceHeight):
        atlasHeight /= 2
        atlasWidth *= 2
    atlasHeight = int(atlasHeight) # Cast back to int after division

    # Create the atlas
    atlas = Image.new("RGBA", (atlasWidth, atlasHeight), (0, 0, 0, 0))

    # Arrange slices into atlas
    slicesPerRow = math.floor(atlasWidth/paddedSliceWidth)

    atlas_index = int(atlas_index)

    # Go through Z-stack, picking planes we want for the requested atlas
    for the_z in range(0, numSlices):
        atlasNumber = the_z % numberOfAtlases
        if atlasNumber != atlas_index:
            continue
        # Calculate position of plane in atlas
        locationIndex = math.floor(the_z/numberOfAtlases)
        xStartPixel = int((locationIndex % slicesPerRow) * paddedSliceWidth + xOffset)
        yStartPixel = math.floor(locationIndex / slicesPerRow) * paddedSliceHeight + yOffset
        yStartPixel = int(atlasHeight - yStartPixel - paddedSliceHeight + 2*yOffset)

        # Render plane and paste onto atlas
        jpeg_data = image.renderJpeg(the_z, 0, compression=0.9)
        plane = Image.open(StringIO(jpeg_data))
        atlas.paste(plane, (xStartPixel, yStartPixel))

    image._re.close()

    output = StringIO()
    atlas.save(output, 'png')
    png_data = output.getvalue()
    output.close()
    return HttpResponse(png_data, content_type='image/png')
