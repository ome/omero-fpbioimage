#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (c) 2017-2018 University of Dundee.
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

"""setup.py for pip installing omero-fpbioimage."""

import os
from setuptools import setup, find_packages
from omero_fpbioimage.version import get_version


def read(fname):
    """
    Utility function to read the README file.

    Used for the long_description.  It's nice, because:
    1) now we have a top level README file
    2) it's easier to type in the README file than to put a raw string in below
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


version = get_version()


setup(name="omero-fpbioimage",
      packages=find_packages(exclude=['ez_setup']),
      version=version,
      description="A Python plugin for OMERO.web",
      long_description=read('README.rst'),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: JavaScript',
          'Programming Language :: Python :: 2',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Internet :: WWW/HTTP :: WSGI',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Software Development :: Libraries :: '
          'Application Frameworks',
          'Topic :: Text Processing :: Markup :: HTML'
      ],  # Get strings from
          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      author='The Open Microscopy Team',
      author_email='ome-devel@lists.openmicroscopy.org.uk',
      license='AGPL-3.0',
      url="https://github.com/ome/omero-fpbioimage",
      download_url='https://github.com/ome/omero-fpbioimage/archive/v%s.tar.gz' % version,  # NOQA
      keywords=['OMERO.web', 'plugin'],
      include_package_data=True,
      zip_safe=False,
      )
