# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015, 2016, 2017 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Multimedia and IIIF Image APIs.

Flask-IIIF is initialized like this:

Initialization of the extension:

>>> from flask import Flask
>>> from flask_iiif import IIIF
>>> app = Flask('myapp')
>>> ext = IIIF(app=app)

or alternatively using the factory pattern:

>>> app = Flask('myapp')
>>> ext = IIIF()
>>> ext.init_app(app)
"""

from __future__ import absolute_import

from flask import current_app

from six import string_types

from werkzeug.urls import url_join
from werkzeug.utils import import_string

from . import config
from .utils import iiif_image_url
from .version import __version__


class IIIF(object):
    """Flask extension implementation."""

    def __init__(self, app=None):
        """Initialize login callback."""
        self.uuid_to_image_opener = None
        self.api_decorator_callback = None
        if app is not None:
            self.init_app(app)

    @staticmethod
    def cache():
        """Return the cache handler.

        .. note::

            You can create your own cache handler by change the
            :py:attr:`~flask_iiif.config.IIIF_CACHE_HANDLER`. More infos
            could be found in :py:mod:`~flask_iiif.cache.cache`.
        """
        from .cache.cache import ImageCache
        handler = current_app.config['IIIF_CACHE_HANDLER']
        if isinstance(handler, string_types):
            handler = import_string(handler)
        if callable(handler):
            handler = handler()
        assert isinstance(handler, ImageCache)
        return handler

    def init_app(self, app):
        """Initialize a Flask application."""
        self.app = app
        # Follow the Flask guidelines on usage of app.extensions
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        if 'iiif' in app.extensions:
            raise RuntimeError("Flask application already initialized")
        app.extensions['iiif'] = self

        # Set default configuration
        for k in dir(config):
            if k.startswith('IIIF_'):
                self.app.config.setdefault(k, getattr(config, k))

        # Register context processors
        if hasattr(app, 'add_template_global'):
            app.add_template_global(iiif_image_url)
        else:
            ctx = dict(
                iiif_image_url=iiif_image_url
            )
            app.context_processor(lambda: ctx)

    def init_restful(self, api, prefix='/api/multimedia/image/'):
        """Set up the urls.

        :param str prefix: the url perfix

        .. note::

            In IIIF Image API the Image Request URI Syntax must following

                ``{scheme}://{server}{/prefix}/{identifier}/
                    {region}/{size}/{rotation}/{quality}.{format}``

            pattern, the default prefix is ``/api/multimedia/image`` but
            this can be changes by changing the ``prefix`` paremeter. The
            ``prefix`` MUST always start and end with `/`

        .. seealso::
            `IIIF IMAGE API URI Syntax
            <http://iiif.io/api/image/2.0/#uri-syntax>`
        """
        from .restful import IIIFImageAPI, IIIFImageInfo, IIIFImageBase

        if not prefix.startswith('/') or not prefix.endswith('/'):
            raise RuntimeError(
                "The `prefix` must always start and end with `/`"
            )

        api.add_resource(
            IIIFImageAPI,
            url_join(
                prefix,
                (
                    "<string:version>/<string:uuid>/"
                    "<string:region>/<string:size>/<string:rotation>/"
                    "<string:quality>.<string:image_format>"
                )
            )
        )

        api.add_resource(
            IIIFImageInfo,
            url_join(
                prefix,
                "<string:version>/<string:uuid>/info.json"
            )
        )
        api.add_resource(
            IIIFImageBase,
            url_join(
                prefix,
                "<string:version>/<string:uuid>"
            )
        )

    def uuid_to_image_opener_handler(self, callback):
        """Set the callback for the ``uuid`` to ``image`` convertion.

        .. note:

            The supported file type is either ``fullpath`` or ``bytestream``
            object anything else will raise
            :class:`~flask_iiif.errors.MultimediaImageNotFound`

        .. code-block:: python

            def uuid_to_path(uuid):
                # do something magical

            iiif.uuid_to_image_opener_handler(uuid_to_path)
        """
        self.uuid_to_image_opener = callback

    def api_decorator_handler(self, callback):
        """Protect API handler.

        .. code-block:: python

            def protect_api():
                return
            iiif.api_decorator_handler(protect_api)

        .. note::

            The API would be always decorated with ``api_decorator_handler``.
            If is not defined, it would just pass.
        """
        self.api_decorator_callback = callback

__all__ = ('IIIF', '__version__')
