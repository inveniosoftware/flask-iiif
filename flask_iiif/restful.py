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

from flask import current_app, jsonify, redirect, send_file, url_for

from flask_restful import Resource
from flask_restful.utils import cors


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


class IIIFImageBase(Resource):

    """IIIF Image Base."""

    def get(self, version, uuid):
        """Get IIIF Image Base.

        .. note::

            It will redirect to ``iiifimageinfo`` endpoint with status code
            303.
        """
        return redirect(
            url_for('iiifimageinfo', version=version, uuid=uuid), code=303
        )


class IIIFImageInfo(Resource):

    """IIIF Image Info."""

    method_decorators = [
        error_handler,
    ]

    @cors.crossdomain(origin='*', methods='GET')
    def get(self, version, uuid):
        """Get IIIF Image Info."""
        # Check if its cached
        cache_handler = current_iiif.cache()

        # build the image key
        key = "iiif:info:{0}/{1}".format(
            version, uuid
        )

        # Check if its cached
        cached = cache_handler.get(key)

        # If the image size is cached loaded from cache
        if cached:
            width, height = map(int, cached.split(','))
        else:
            data = current_iiif.uuid_to_image_opener(uuid)
            image = IIIFImageAPIWrapper.open_image(data)
            width, height = image.size()
            cache_handler.set(key, "{0},{1}".format(width, height))

        data = current_app.config['IIIF_API_INFO_RESPONSE_SKELETON'][version]

        base_uri = url_for(
            'iiifimagebase',
            uuid=uuid,
            version=version,
            _external=True
        )
        data["@id"] = base_uri
        data["width"] = width
        data["height"] = height
        return jsonify(data)


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
