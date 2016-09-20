# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Flask-IIIF test helpers."""

from contextlib import contextmanager
from io import BytesIO

from flask import Flask, abort, url_for
from flask_testing import TestCase


class IIIFTestCase(TestCase):

    """IIIF REST test case."""

    def create_app(self):
        """Create the app."""
        from flask_iiif import IIIF
        from flask_restful import Api
        from flask_iiif.cache.simple import ImageSimpleCache

        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = "shield.worker.node.1"
        app.config['SITE_URL'] = "http://shield.worker.node.1"
        app.config['IIIF_CACHE_HANDLER'] = ImageSimpleCache()
        app.logger.disabled = True

        api = Api(app=app)

        iiif = IIIF(app=app)

        iiif.uuid_to_image_opener_handler(self.create_image)

        def api_decorator_test(*args, **kwargs):
            if 'decorator' in kwargs.get('uuid'):
                abort(403)

        iiif.api_decorator_handler(api_decorator_test)

        iiif.init_restful(api)
        return app

    def get(self, *args, **kwargs):
        """Simulate a GET request."""
        return self.make_request(self.client.get, *args, **kwargs)

    def post(self, *args, **kwargs):
        """Simulate a POST request."""
        return self.make_request(self.client.post, *args, **kwargs)

    def put(self, *args, **kwargs):
        """Simulate a PUT request."""
        return self.make_request(self.client.put, *args, **kwargs)

    def delete(self, *args, **kwargs):
        """Simulate a DELETE request."""
        return self.make_request(self.client.delete, *args, **kwargs)

    def patch(self, *args, **kwargs):
        """Simulate a PATCH request."""
        return self.make_request(self.client.patch, *args, **kwargs)

    def make_request(self, client_func, endpoint, urlargs=None):
        """Simulate a request."""
        url = url_for(endpoint, **(urlargs or {}))
        response = client_func(
            url,
            base_url=self.app.config['SITE_URL']
        )
        return response

    def create_image(self, uuid):
        """Create a test image."""
        if uuid.startswith('valid'):
            from PIL import Image
            tmp_file = BytesIO()
            # create a new image
            image = Image.new("RGBA", (1280, 1024), (255, 0, 0, 0))
            image.save(tmp_file, 'png')
            tmp_file.seek(0)
            return tmp_file
        return ''


@contextmanager
def signal_listener(signal):
    """Context Manager that listen to signals.

    .. note::

        Checks if any signal were fired and returns the passed arguments.

    .. code-block:: python

        from somesignals import signal

        with signal_listener(signal) as listener:
            fire_the_signal()
            results = listener.assert_signal()
            # Assert the results here

    """
    class _Signal(object):
        def __init__(self):
            self.heard = []

        def add(self, *args, **kwargs):
            """Keep the signals."""
            self.heard.append((args, kwargs))

        def assert_signal(self):
            """Check signal."""
            if len(self.heard) == 0:
                raise AssertionError("No signals.")
            return self.heard[0][0], self.heard[0][1]

    signals = _Signal()
    signal.connect(signals.add)

    try:
        yield signals
    finally:
        signal.disconnect(signals.add)
