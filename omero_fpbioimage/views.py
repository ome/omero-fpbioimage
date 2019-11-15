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

import math
from PIL import Image
from io import BytesIO


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
    scale = 1.0

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

    slice_width = image.getSizeX()
    slice_height = image.getSizeY()

    # If > 512 * 512 need to scale down
    max_size = 512
    if slice_width > max_size or slice_height > max_size:
        longest_side = max(slice_width, slice_height)
        slice_width = (slice_width * max_size) / longest_side
        slice_height = (slice_height * max_size) / longest_side
        scale = float(max_size) / longest_side

    context = {'image_name': image.getName(),
               'image_id': image.id,
               'slice_width': slice_width,
               'slice_height': slice_height,
               'slice_count': image.getSizeZ(),
               'size_x': x * scale,
               'size_y': y * scale,
               'size_z': z * scale
               }
    return render(request, 'fpbioimage/viewer.html', context)


def ceil2(x):
    # Round up to the next power of 2
    return 1 << (x - 1).bit_length()


@login_required()
def fpbioimage_png(request, image_id, atlas_index, conn=None, **kwargs):
    """Render png for image at specified Z section."""
    image = conn.getObject('image', image_id)

    slice_width = image.getSizeX()
    slice_height = image.getSizeY()

    # If > 512 * 512 need to scale down
    max_size = 512
    if slice_width > max_size or slice_height > max_size:
        longest_side = max(slice_width, slice_height)
        slice_width = (slice_width * max_size) / longest_side
        slice_height = (slice_height * max_size) / longest_side

    num_slices = image.getSizeZ()

    # Set for FPBioimage v4
    number_of_atlases = 8

    # Calculate necessary variables
    padded_slice_width = ceil2(slice_width)
    padded_slice_height = ceil2(slice_height)

    x_offset = math.floor((padded_slice_width-slice_width)/2)
    y_offset = math.floor((padded_slice_height-slice_height)/2)

    slices_per_atlas = math.ceil(num_slices/number_of_atlases)
    atlas_width = ceil2(padded_slice_width)
    atlas_height = ceil2(int(padded_slice_height * slices_per_atlas))
    while (atlas_height > 2*atlas_width) & (atlas_height > slice_height):
        atlas_height /= 2
        atlas_width *= 2
    atlas_height = int(atlas_height)

    # Create the atlas
    atlas = Image.new("RGBA", (atlas_width, atlas_height), (0, 0, 0, 0))

    # Arrange slices into atlas
    slices_per_row = math.floor(atlas_width/padded_slice_width)
    atlas_index = int(atlas_index)

    # Go through Z-stack, picking planes we want for the requested atlas
    for the_z in range(0, num_slices):
        atlas_number = the_z % number_of_atlases
        if atlas_number != atlas_index:
            continue
        # Calculate position of plane in atlas
        location_index = math.floor(the_z/number_of_atlases)
        x_start_pixel = int((location_index % slices_per_row) *
                            padded_slice_width + x_offset)
        y_start_pixel = (math.floor(location_index / slices_per_row) *
                         padded_slice_height + y_offset)
        y_start_pixel = int(atlas_height - y_start_pixel -
                            padded_slice_height + 2*y_offset)

        # Render plane and paste onto atlas
        jpeg_data = image.renderJpeg(the_z, 0, compression=0.9)
        plane = Image.open(BytesIO(jpeg_data))
        if plane.size[0] > slice_width:
            plane = plane.resize((slice_width, slice_height), Image.BICUBIC)
        atlas.paste(plane, (x_start_pixel, y_start_pixel))

    # in case there weren't any planes for current atlas_index (small sizeZ)
    if image._re is not None:
        image._re.close()

    output = BytesIO()
    atlas.save(output, 'png')
    png_data = output.getvalue()
    output.close()
    return HttpResponse(png_data, content_type='image/png')
