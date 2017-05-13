#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns('django.views.generic.simple',

    # index
    url(r'^$', views.index, name='fpbioimage_index'),

    url(r'^viewer/(?P<image_id>[0-9]+)/', views.fpbioimage, name='fpbioimage_viewer'),

    url(r'^imageStacks/(?P<image_id>[0-9]+)/(?P<theZ>[0-9]+)\.png', views.fpbioimage_png,
        name='fpbioimage_png'),

    url(r'^viewer//fpbioimage/imageStacks/(?P<image_id>[0-9]+)/(?P<theZ>[0-9]+)\.png', views.fpbioimage_png,
        name='fpbioimage_png2'),
)
