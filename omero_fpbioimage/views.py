
from django.http import HttpResponse
from django.shortcuts import render
from omeroweb.webclient.decorators import login_required

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


@login_required()
def fpbioimage_png(request, image_id, the_z, conn=None, **kwargs):
    """Render png for image at specified Z section."""
    image = conn.getObject('image', image_id)
    jpeg_data = image.renderJpeg(the_z, 0, compression=0.9)
    i = Image.open(StringIO(jpeg_data))
    size_x = image.getSizeX()
    size_y = image.getSizeY()
    def_w = 500
    def_h = 500
    width = def_w
    height = def_h
    resize = False

    if size_x > def_w:
        width = def_w
        resize = True
    if size_y > def_h:
        height = def_h
        resize = True
    if resize:
        r = float(size_x)/float(size_y)
        if r < 1:
            width = int(width*r)
        else:
            height = int(height/r)
        i = i.resize((width, height), PIL.Image.ANTIALIAS)
    output = StringIO()
    i.save(output, 'png')
    png_data = output.getvalue()
    output.close()
    return HttpResponse(png_data, content_type='image/png')
