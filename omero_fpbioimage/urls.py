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

from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns(

    'django.views.generic.simple',

    # index placeholder
    url(r'^$', views.index, name='fpbioimage_index'),

    # Viewer page
    url(r'^viewer/(?P<image_id>[0-9]+)/', views.fpbioimage,
        name='fpbioimage_viewer'),

    # PNG plane. This is used for 'first_image'
    url(r'^imageStacks/(?P<image_id>[0-9]+)/(?P<the_z>[0-9]+)\.png',
        views.fpbioimage_png, name='fpbioimage_png'),

    # PNG planes to load whole stack.
    # Can't seem to control how this url is generated in JavaScript from
    # the 'first_image' url above. So it's ugly but this works for now.
    url(r'^viewer//fpbioimage/imageStacks/'
        '(?P<image_id>[0-9]+)/(?P<the_z>[0-9]+)\.png',
        views.fpbioimage_png, name='fpbioimage_png2'),
)
