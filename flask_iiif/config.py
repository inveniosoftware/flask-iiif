# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""IIIF configuration.

.. py:data:: IIIF_CACHE_HANDLER

    Add the prefered cache adaptor.

    .. seealso:: :py:class:`~flask_iiif.cache.cache.ImageCache`

.. py:data:: IIIF_CACHE_TIME

    How much time the image would be cached.

.. py:data:: IIIF_QUALITIES

    The supported image qualities.

    .. seealso::

            `IIIF Image API
            <http://iiif.io/api/image/2.0/#quality>`_

.. py:data:: IIIF_CONVERTERS

    The supported image converters.

.. py:data: IIIF_FORMATS

    The supported image formats with their MIME type.

.. py:data:: IIIF_VALIDATIONS

    The IIIF Image API validation.

    .. seealso::

        `IIIF Image API v1
        <http://iiif.io/api/image/1.1/>`_ and
        `IIIF Image API v2
        <http://iiif.io/api/image/2.0/>`_

"""
# Cache handler
IIIF_CACHE_HANDLER = 'flask_iiif.cache.simple:ImageSimpleCache'

# Cache duration
# 60 seconds * 60 minutes (1 hour) * 24 (24 hours) * 2 (2 days) = 172800 secs
# 60 seconds * 60 (1 hour) * 24 (1 day) * 2 (2 days)
IIIF_CACHE_TIME = 60 * 60 * 24 * 2

# Supported qualities
IIIF_QUALITIES = (
    'default', 'grey', 'bitonal', 'color', 'native'
)
# Suported coverters
IIIF_CONVERTERS = '', 'L', '1', '', ''

# Supported multimedia image API formats
IIIF_FORMATS = {
    'gif': 'image/gif',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'pdf': 'application/pdf',
    'png': 'image/png',
}

# Regular expressions to validate each parameter
IIIF_VALIDATIONS = {
    "v1": {
        "region": {
            "ignore": "full",
            "validate": "(^full|(pct:)?([\d.]+,){3}([\d.]+))",
        },
        "size": {
            "ignore": "full",
            "validate": ("(^full|[\d.]+,|,[\d.]+|pct:[\d.]+|[\d.]+,"
                         "[\d.]+|![\d.]+,[\d.]+)")
        },
        "rotate": {
            "ignore": "0",
            "validate": "^[\d.]+$"
        },
        "quality": {
            "ignore": "default",
            "validate": "(native|color|grey|bitonal)"
        },
        "image_format": {
            "ignore": "",
            "validate": "(jpg|png|gif|jp2|jpeg|pdf)"
        }
    },
    "v2": {
        "region": {
            "ignore": "full",
            "validate": "(^full|(pct:)?([\d.]+,){3}([\d.]+))",
        },
        "size": {
            "ignore": "full",
            "validate": ("(^full|[\d.]+,|,[\d.]+|pct:[\d.]+|[\d.]+,"
                         "[\d.]+|![\d.]+,[\d.]+)")
        },
        "rotate": {
            "ignore": "0",
            "validate": "^!?[\d.]+$"
        },
        "quality": {
            "ignore": "default",
            "validate": "(default|color|grey|bitonal)"
        },
        "image_format": {
            "ignore": "",
            "validate": "(jpg|png|gif|jp2|jpeg|pdf)"
        }
    }
}

# Qualities per image mode
IIIF__MODE = {
    '1': ['default', 'bitonal'],
    'L': ['default', 'gray', 'bitonal'],
    'P': ['default', 'gray', 'bitonal'],
    'RGB': ['default', 'color', 'gray', 'bitonal'],
    'RGBA': ['default', 'color', 'gray', 'bitonal'],
    'CMYK': ['default', 'color', 'gray', 'bitonal'],
    'YCbCr': ['default', 'color', 'gray', 'bitonal'],
    'I': ['default', 'color', 'gray', 'bitonal'],
    'F': ['default', 'color', 'gray', 'bitonal']
}
