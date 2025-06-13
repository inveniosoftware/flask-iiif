# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015, 2016, 2017 CERN.
# Copyright (C) 2020 data-futures.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""IIIF configuration.

.. py:data:: IIIF_CACHE_HANDLER

    Add the preferred cache adaptor.

    .. seealso:: :py:class:`~flask_iiif.cache.cache.ImageCache`

.. py:data:: IIIF_CACHE_REDIS_PREFIX

    Sets prefix for redis keys, default: `iiif`

.. py:data:: IIIF_CACHE_TIME

    How much time the image would be cached.

.. py:data:: IIIF_QUALITIES

    The supported image qualities.

    .. seealso::

            `IIIF Image API
            <http://iiif.io/api/image/2.0/#quality>`_

.. py:data:: IIIF_CONVERTERS

    The supported image converters.

.. py:data:: IIIF_FORMATS

    The supported image formats with their MIME type.

.. py:data:: IIIF_VALIDATIONS

    The IIIF Image API validation.

    .. seealso::

        `IIIF Image API v1
        <http://iiif.io/api/image/1.1/>`_ and
        `IIIF Image API v2
        <http://iiif.io/api/image/2.0/>`_

.. py:data:: IIIF_API_INFO_RESPONSE_SKELETON

    Information request document for the image.

    .. seealso::
        `IIIF Image API v1 Information request
        <http://iiif.io/api/image/1.1/#information-request>`_ and
        `IIIF Image API v2 Information request
        <http://iiif.io/api/image/2.0/#information-request>`_

"""
# Cache handler
IIIF_CACHE_HANDLER = "flask_iiif.cache.simple:ImageSimpleCache"

# Cache duration
# 60 seconds * 60 minutes (1 hour) * 24 (24 hours) * 2 (2 days) = 172800 secs
# 60 seconds * 60 (1 hour) * 24 (1 day) * 2 (2 days)
IIIF_CACHE_TIME = 60 * 60 * 24 * 2

# Redis URL Cache
IIIF_CACHE_REDIS_URL = "redis://localhost:6379/0"

# Supported qualities
IIIF_QUALITIES = ("default", "gray", "grey", "bitonal", "color", "native")
# Suported coverters
IIIF_CONVERTERS = "", "L", "L", "1", "", ""

# Supported multimedia image API formats
IIIF_FORMATS = {
    "gif": "image/gif",
    "jp2": "image/jp2",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "pdf": "application/pdf",
    "png": "image/png",
    "tif": "image/tiff",
    "tiff": "image/tiff",
    "webp": "image/webp",
}

IIIF_FORMATS_PIL_MAP = {
    "gif": "gif",
    "jp2": "jpeg2000",
    "jpeg": "jpeg",
    "jpg": "jpeg",
    "pdf": "pdf",
    "png": "png",
    "tif": "tiff",
    "tiff": "tiff",
    "webp": "webp",
}

# Regular expressions to validate each parameter
IIIF_VALIDATIONS = {
    "v1": {
        "region": {
            "ignore": "full",
            "validate": r"(^full|(pct:)?([\d.]+,){3}([\d.]+))",
        },
        "size": {
            "ignore": "full",
            "validate": (
                r"(^full|[\d.]+,|,[\d.]+|pct:[\d.]+|[\d.]+,[\d.]+|![\d.]+,[\d.]+)"
            ),
        },
        "rotation": {"ignore": "0", "validate": r"^[\d.]+$"},
        "quality": {"ignore": "default", "validate": r"(native|color|gr[ae]y|bitonal)"},
        "image_format": {
            "ignore": "",
            "validate": r"(gif|jp2|jpe?g|pdf|png|tiff?|webp)",
        },
    },
    "v2": {
        "region": {
            "ignore": "full",
            "validate": r"(^full|(pct:)?([\d.]+,){3}([\d.]+))",
        },
        "size": {
            "ignore": "full",
            "validate": (
                r"(^full|[\d.]+,|,[\d.]+|pct:[\d.]+|[\d.]+,[\d.]+|![\d.]+,[\d.]+)"
            ),
        },
        "rotation": {"ignore": "0", "validate": r"^!?[\d.]+$"},
        "quality": {
            "ignore": "default",
            "validate": r"(default|color|gr[ae]y|bitonal)",
        },
        "image_format": {
            "ignore": "",
            "validate": r"(gif|jp2|jpe?g|pdf|png|tiff?|webp)",
        },
    },
}

# Qualities per image mode
IIIF_MODE = {
    "1": ["default", "bitonal"],
    "L": ["default", "gray", "grey", "bitonal"],
    "P": ["default", "gray", "grey", "bitonal"],
    "RGB": ["default", "color", "gray", "grey", "bitonal"],
    "RGBA": ["default", "color", "gray", "grey", "bitonal"],
    "CMYK": ["default", "color", "gray", "grey", "bitonal"],
    "YCbCr": ["default", "color", "gray", "grey", "bitonal"],
    "I": ["default", "color", "gray", "grey", "bitonal"],
    "F": ["default", "color", "gray", "grey", "bitonal"],
}

# API Info
IIIF_API_INFO_RESPONSE_SKELETON = {
    "v1": {
        "@context": ("http://library.stanford.edu/iiif/image-api/1.1/context.json"),
        "@id": "",
        "width": "",
        "height": "",
        "profile": (
            "http://library.stanford.edu/iiif/image-api/compliance.html#level1"
        ),
        "tile_width": 256,
        "tile_height": 256,
        "scale_factors": [1, 2, 4, 8, 16, 32, 64],
    },
    "v2": {
        "@context": "http://iiif.io/api/image/2/context.json",
        "@id": "",
        "protocol": "http://iiif.io/api/image",
        "width": "",
        "height": "",
        "tiles": [{"width": 256, "scaleFactors": [1, 2, 4, 8, 16, 32, 64]}],
        "profile": ["http://iiif.io/api/image/2/level2.json"],
    },
}

# Raise errors during interactions with the cache.
IIIF_CACHE_IGNORE_ERRORS = False

IIIF_GIF_TEMP_FOLDER_PATH = "/tmp"
