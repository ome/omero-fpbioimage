.. image:: https://travis-ci.org/ome/omero-fpbioimage.svg?branch=master
    :target: https://travis-ci.org/ome/omero-fpbioimage

.. image:: https://badge.fury.io/py/omero-fpbioimage.svg
    :target: https://badge.fury.io/py/omero-fpbioimage

OMERO FPBioimage
================

FPBioImage as an OMERO.web app.

Requirements
============

* OMERO 5.2.6 or newer.

Installing from PyPI
====================

This section assumes that an OMERO.web is already installed.

Install the app using `pip <https://pip.pypa.io/en/stable/>`_:

::

    $ pip install omero-fpbioimage

Add fpbioimage custom app to your installed web apps:

::

    $ bin/omero config append omero.web.apps '"omero_fpbioimage"'

Optionally add fpbioimage to the 'Open with' config, to enable
open-with menu for Images in OMERO.webclient:

::

    $ bin/omero config append omero.web.open_with '["omero_fpbioimage", "fpbioimage_index",
      {"script_url": "fpbioimage/openwith.js", "supported_objects": ["image"], "label": "FPBioimage"}]'

Now restart OMERO.web as normal.


License
-------

TODO.

Copyright
---------

2017, The Open Microscopy Environment