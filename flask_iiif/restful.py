# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015, 2016, 2017 CERN.
# Copyright (C) 2020 data-futures.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Multimedia IIIF Image API."""
import datetime
from email.utils import parsedate
from io import BytesIO

from flask import Response, current_app, jsonify, redirect, request, \
    send_file, url_for
from flask_restful import Resource
from flask_restful.utils import cors
from werkzeug.local import LocalProxy
from werkzeug.utils import secure_filename

from .api import IIIFImageAPIWrapper
from .decorators import api_decorator, error_handler
from .signals import iiif_after_info_request, iiif_after_process_request, \
    iiif_before_info_request, iiif_before_process_request
from .utils import should_cache

current_iiif = LocalProxy(lambda: current_app.extensions["iiif"])


class IIIFImageBase(Resource):
    """IIIF Image Base."""

    def get(self, version, uuid):
        """Get IIIF Image Base.

        .. note::

            It will redirect to ``iiifimageinfo`` endpoint with status code
            303.
        """
        return redirect(url_for("iiifimageinfo", version=version, uuid=uuid), code=303)


class IIIFImageInfo(Resource):
    """IIIF Image Info."""

    method_decorators = [
        error_handler,
        api_decorator,
    ]

    @cors.crossdomain(origin="*", methods="GET")
    def get(self, version, uuid):
        """Get IIIF Image Info."""
        # Trigger event before proccess the api request
        iiif_before_info_request.send(self, version=version, uuid=uuid)

        # build the image key
        key = u"iiif:info:{0}/{1}".format(version, uuid)

        # Check if its cached
        try:
            cached = current_iiif.cache.get(key)
        except Exception:
            if current_app.config.get("IIIF_CACHE_IGNORE_ERRORS", False):
                cached = None
            else:
                raise

        # If the image size is cached loaded from cache
        if cached:
            width, height = map(int, cached.split(","))
        else:
            data = current_iiif.uuid_to_image_opener(uuid)
            image = IIIFImageAPIWrapper.open_image(data)
            width, height = image.size()
            image.close_image()
            if should_cache(request.args):
                try:
                    current_iiif.cache.set(key, "{0},{1}".format(width, height))
                except Exception:
                    if not current_app.config.get("IIIF_CACHE_IGNORE_ERRORS", False):
                        raise

        data = current_app.config["IIIF_API_INFO_RESPONSE_SKELETON"][version]

        base_uri = url_for("iiifimagebase", uuid=uuid, version=version, _external=True)
        data["@id"] = base_uri
        data["width"] = width
        data["height"] = height

        # Trigger event after proccess the api request
        iiif_after_info_request.send(self, **data)

        resp = jsonify(data)
        if "application/ld+json" in request.headers.get("Accept", ""):
            resp.mimetype = "application/ld+json"
        return resp


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

    def get(self, version, uuid, region, size, rotation, quality, image_format):
        """Run IIIF Image API workflow."""
        api_parameters = dict(
            version=version,
            uuid=uuid,
            region=region,
            size=size,
            rotation=rotation,
            quality=quality,
            image_format=image_format,
        )
        # Trigger event before proccess the api request
        iiif_before_process_request.send(self, **api_parameters)

        # Validate IIIF parameters
        IIIFImageAPIWrapper.validate_api(**api_parameters)

        # build the image key
        key = u"iiif:{0}/{1}/{2}/{3}/{4}.{5}".format(
            uuid, region, size, quality, rotation, image_format
        )

        # Check if its cached
        try:
            cached = current_iiif.cache.get(key)
        except Exception:
            if current_app.config.get("IIIF_CACHE_IGNORE_ERRORS", False):
                cached = None
            else:
                raise

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
                quality=quality,
            )

            # prepare image to be serve
            to_serve = image.serve(image_format=image_format)
            image.close_image()
            if should_cache(request.args):
                try:
                    current_iiif.cache.set(key, to_serve.getvalue())
                except Exception:
                    if not current_app.config.get("IIIF_CACHE_IGNORE_ERRORS", False):
                        raise

        try:
            last_modified = current_iiif.cache.get_last_modification(key)
        except Exception:
            if not current_app.config.get("IIIF_CACHE_IGNORE_ERRORS", False):
                raise
            last_modified = None

        # decide the mime_type from the requested image_format
        mimetype = current_app.config["IIIF_FORMATS"].get(image_format, "image/jpeg")
        # Built the after request parameters
        api_after_request_parameters = dict(mimetype=mimetype, image=to_serve)

        # Trigger event after proccess the api request
        iiif_after_process_request.send(self, **api_after_request_parameters)
        send_file_kwargs = {"mimetype": mimetype}
        # last_modified is not supported before flask 0.12
        additional_headers = []
        if last_modified:
            send_file_kwargs.update(last_modified=last_modified)

        if "dl" in request.args:
            filename = secure_filename(request.args.get("dl", ""))
            if filename.lower() in {"", "1", "true"}:
                filename = u"{0}-{1}-{2}-{3}-{4}.{5}".format(
                    uuid, region, size, quality, rotation, image_format
                )
            send_file_kwargs.update(
                as_attachment=True, attachment_filename=secure_filename(filename),
            )
        if_modified_since_raw = request.headers.get("If-Modified-Since")
        if if_modified_since_raw:
            if_modified_since = datetime.datetime(*parsedate(if_modified_since_raw)[:6])
            if if_modified_since and if_modified_since >= last_modified:
                return Response(status=304)
        response = send_file(to_serve, **send_file_kwargs)
        if additional_headers:
            response.headers.extend(additional_headers)
        return response
