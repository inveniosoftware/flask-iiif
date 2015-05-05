# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Multimedia IIIF Image API."""

from io import BytesIO

from flask import current_app, send_file
from flask.ext.restful import Resource, abort

from werkzeug import LocalProxy


from .api import (
    IIIFImageAPIWrapper
)

from .decorators import (
    api_decorator, error_handler
)

from .signals import (
    iiif_after_process_request, iiif_before_process_request
)

current_iiif = LocalProxy(lambda: current_app.extensions['iiif'])


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
        api_decorator,
    ]

    def get(self, version, uuid, region, size, rotation, quality,
            image_format):
        """Run IIIF Image API workflow."""
        api_parameters = dict(
            version=version,
            uuid=uuid,
            region=region,
            size=size,
            rotation=rotation,
            quality=quality,
            image_format=image_format
        )
        # Trigger event before proccess the api request
        iiif_before_process_request.send(self, **api_parameters)

        # Validate IIIF parameters
        IIIFImageAPIWrapper.validate_api(**api_parameters)

        cache_handler = current_iiif.cache()

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
        # Otherwise create the image
        else:
            data = current_iiif.uuid_to_image_opener(uuid)
            image = IIIFImageAPIWrapper.open_image(data)

            image.apply_api(
                version=version,
                region=region,
                size=size,
                rotation=rotation,
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
        # Built the after request parameters
        api_after_request_parameters = dict(
            mimetype=mimetype,
            image=to_serve
        )

        # Trigger event after proccess the api request
        iiif_after_process_request.send(self, **api_after_request_parameters)

        # Built the after request parameters
        api_after_request_parameters = dict(
            mimetype=mimetype,
            image=to_serve
        )

        # Trigger event after proccess the api request
        iiif_after_process_request.send(self, **api_after_request_parameters)
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
