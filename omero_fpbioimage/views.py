
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
    width = max(image.getSizeX(), image.getSizeY())
    if width > 500:
        width = 500
    i = Image.open(StringIO(jpeg_data))
    p = (width/float(i.size[0]))
    hsize = int((float(i.size[1])*float(p)))
    i = i.resize((width, hsize), PIL.Image.ANTIALIAS)
    output = StringIO()
    i.save(output, 'png')
    png_data = output.getvalue()
    output.close()
    return HttpResponse(png_data, content_type='image/png')
