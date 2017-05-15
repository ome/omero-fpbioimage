
from django.http import HttpResponse
from django.shortcuts import render
from omeroweb.webclient.decorators import login_required

from PIL import Image
from cStringIO import StringIO


def index(request):

    return HttpResponse("FPBioimage Index")


@login_required()
def fpbioimage(request, iid, conn=None, **kwargs):
    """Load the viewer page for the image."""
    image = conn.getObject('image', iid)
    context = {'image': image}

    return render(request, 'fpbioimage/viewer.html', context)


@login_required()
def fpbioimage_png(request, iid, the_z, conn=None, **kwargs):
    """Render png for image at specified Z section."""
    image = conn.getObject('image', iid)
    jpeg_data = image.renderJpeg(the_z, 0, compression=0.9)

    i = Image.open(StringIO(jpeg_data))
    output = StringIO()
    i.save(output, 'png')
    png_data = output.getvalue()
    output.close()
    return HttpResponse(png_data, content_type='image/png')
