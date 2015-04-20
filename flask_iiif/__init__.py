# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015 CERN.
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

from werkzeug.utils import import_string

from . import config
from .utils import iiif_image_url
from .version import __version__


class IIIF(object):

    """Flask extension implementation."""

    def __init__(self, app=None):
        """Initialize login callback."""
        self.uuid_to_path = None

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
        handler = current_app.config['IIIF_CACHE_HANDLER']
        return (
            import_string(handler) if isinstance(handler, string_types)
            else handler
        )

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

    def init_restful(self, api):
        """Setup the urls."""
        from .restful import IIIFImageAPI

        api.add_resource(
            IIIFImageAPI,
            ("/api/multimedia/image/<string:version>/<string:uuid>/"
             "<string:region>/<string:size>/<string:rotation>/"
             "<string:quality>.<string:image_format>"),
        )

    def uuid_to_path_handler(self, callback):
        """Set the callback for the ``uuid`` to ``path`` convertion.

        :param callback: The callback for login.
        :type callback: function
        """
        self.uuid_to_path = callback


__all__ = ('IIIF', '__version__')
