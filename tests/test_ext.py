# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

from __future__ import absolute_import

import six

from .helpers import FlaskTestCase

from contextlib import contextmanager
from flask import request_started, request
from flask_iiif import IIIF, config as default_config


class TestIIIF(FlaskTestCase):

    """Test extension creation."""

    def test_version(self):
        """Assert that version number can be parsed."""
        from flask_iiif import __version__
        from distutils.version import LooseVersion
        LooseVersion(__version__)

    def test_creation(self):
        assert 'iiif' not in self.app.extensions
        IIIF(app=self.app)
        assert isinstance(self.app.extensions['iiif'], IIIF)

    def test_creation_old_flask(self):
        """Simulate old Flask (pre 0.9)."""
        del self.app.extensions
        IIIF(app=self.app)
        assert isinstance(self.app.extensions['iiif'], IIIF)

    def test_creation_init(self):
        assert 'iiif' not in self.app.extensions
        r = IIIF()
        r.init_app(app=self.app)
        assert isinstance(self.app.extensions['iiif'], IIIF)

    def test_double_creation(self):
        IIIF(app=self.app)
        self.assertRaises(RuntimeError, IIIF, app=self.app)

    def test_default_config(self):
        IIIF(app=self.app)
        for k in dir(default_config):
            if k.startswith('IIIF_'):
                assert self.app.config.get(k) == getattr(default_config, k)
