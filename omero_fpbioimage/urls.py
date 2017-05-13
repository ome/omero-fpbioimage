#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns('django.views.generic.simple',

    # index placeholder
    url(r'^$', views.index, name='fpbioimage_index'),

    # Viewer page
    url(r'^viewer/(?P<image_id>[0-9]+)/', views.fpbioimage, name='fpbioimage_viewer'),

    # PNG plane. This is used for 'first_image'
    url(r'^imageStacks/(?P<image_id>[0-9]+)/(?P<theZ>[0-9]+)\.png', views.fpbioimage_png,
        name='fpbioimage_png'),
    # PNG planes to load whole stack.
    # Can't seem to control how this url is generated in JavaScript from
    # the 'first_image' url above. So it's ugly but this works for now.
    url(r'^viewer//fpbioimage/imageStacks/(?P<image_id>[0-9]+)/(?P<theZ>[0-9]+)\.png', views.fpbioimage_png,
        name='fpbioimage_png2'),
)
