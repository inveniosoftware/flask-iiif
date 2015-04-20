# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2015 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Flask-IIIF utilities."""

from flask import abort, url_for

__all__ = ('iiif_image_url', )


def iiif_image_url(**kwargs):
    """Generate a `IIIF API` image url.

    :returns: `IIIF API` image url
    :rtype: str

    .. code:: html

        <img
            src="{{ iiif_image_url(uuid="id", size="200,200") }}"
            alt="Title"
        />

    .. note::

        If any IIIF parameter missing it will fall back to default:
        * `image_format = png`
        * `quality = default`
        * `region = full`
        * `rotation = 0`
        * `size = full`
        * `version = v2`
    """
    try:
        assert kwargs.get('uuid') is not None
    except AssertionError:
        abort(404)
    else:
        return url_for(
            'iiifimageapi',
            image_format=kwargs.get('image_format', 'png'),
            quality=kwargs.get('quality', 'default'),
            region=kwargs.get('region', 'full'),
            rotation=kwargs.get('rotation', 0),
            size=kwargs.get('size', 'full'),
            uuid=kwargs.get('uuid'),
            version=kwargs.get('version', 'v2'),
        )
