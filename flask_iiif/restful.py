# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Multimedia IIIF Image API."""

from flask import current_app, send_file
from flask.ext.restful import abort, Resource
from functools import wraps
from io import BytesIO

from .api import (
    IIIFImageAPIWrapper
)

from .errors import (
    MultimediaError, MultmediaImageCropError, MultmediaImageResizeError,
    MultimediaImageFormatError, MultimediaImageRotateError,
    MultimediaImageQualityError, IIIFValidatorError, MultimediaImageNotFound,
    MultimediaImageForbidden
)


def error_handler(f):
    """error handler."""
    @wraps(f)
    def inner(*args, **kwargs):
        """wrap the errors."""
        try:
            return f(*args, **kwargs)
        except (MultmediaImageCropError, MultmediaImageResizeError,
                MultimediaImageFormatError, MultimediaImageRotateError,
                MultimediaImageQualityError) as error:
            abort(500, message=error.message, code=500)
        except IIIFValidatorError as error:
            abort(400, message=error.message, code=400)
        except (MultimediaError, MultimediaImageNotFound,
                MultimediaImageForbidden) as error:
            abort(error.code, message=error.message, code=error.code)
    return inner


class IIIFImageAPI(Resource):

    """IIIF API Implementation.

    .. note::

        * IIF IMAGE API v1.0
            * For more infos please visit <http://iiif.io/api/image/>.
        * IIIF Image API v2.0
            * For more infos please visit <http://iiif.io/api/image/2.0/>.
        * The API works only for GET requests
        * The image process must follow strictly the following workflow:

           * Region
           * Size
           * Rotation
           * Quality
           * Format

    """

    method_decorators = [
        error_handler,
    ]

    def get(self, version, uuid, region, size, rotation, quality,
            image_format):
        """Run IIIF Image API workflow."""
        # Validate IIIF parameters
        IIIFImageAPIWrapper.validate_api(
            version=version,
            region=region,
            size=size,
            rotate=rotation,
            quality=quality,
            image_format=image_format
        )

        cache_handler = current_app.extensions['iiif'].cache()

        # build the image key
        key = "iiif:{0}/{1}/{2}/{3}/{4}.{5}".format(
            uuid, region, size, quality, rotation, image_format
        )

        # Check if its cached
        cached = cache_handler.get(key)

        # If the image is cached loaded from cache
        if cached:
            to_serve = BytesIO(cached)
            to_serve.seek(0)
        # Otherwise build create the image
        else:
            path = current_app.extensions['iiif'].uuid_to_path(uuid)
            image = IIIFImageAPIWrapper.from_file(path)

            image.apply_api(
                version=version,
                region=region,
                size=size,
                rotate=rotation,
                quality=quality
            )

            # prepare image to be serve
            to_serve = image.serve(image_format=image_format)
            # to_serve = image.serve(image_format=image_format)
            cache_handler.set(key, to_serve.getvalue())

        # decide the mime_type from the requested image_format
        mimetype = current_app.config['IIIF_FORMATS'].get(
            image_format, 'image/jpeg'
        )
        return send_file(to_serve, mimetype=mimetype)

    def post(self):
        """post."""
        abort(405)

    def delete(self):
        """delete."""
        abort(405)

    def options(self):
        """options."""
        abort(405)

    def put(self):
        """put."""
        abort(405)

    def head(self):
        """head."""
        abort(405)
