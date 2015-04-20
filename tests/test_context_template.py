# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2015 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Context Template Tests."""

from unittest import TestCase

from flask import Flask


class TestContextTemplates(TestCase):

    """Context templates test case."""

    def setUp(self):
        """Run before the test."""
        # Create an image in memory
        from flask_iiif import IIIF
        from flask_restful import Api

        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = "happy.fake.server"
        app.logger.disabled = True

        api = Api(app=app)

        iiif = IIIF(app=app)
        iiif.init_restful(api)

        self.app = app

    def tearDown(self):
        """Run after the test."""
        self.app = None

    def test_context_tempalte_iiif_image_url(self):
        """Test context template."""
        from werkzeug.exceptions import NotFound
        from flask_iiif.utils import iiif_image_url

        with self.app.app_context():
            image_url_default = iiif_image_url(
                uuid="test"
            )
            image_url_default_answer = (
                "http://happy.fake.server/api/multimedia/image/v2/test/full"
                "/full/0/default.png"
            )
            self.assertEqual(
                image_url_default_answer,
                image_url_default
            )
            image_url_custom_answer = (
                "http://happy.fake.server/api/multimedia/image/v1/test/full"
                "/full/180/default.jpg"
            )
            image_url_custom = iiif_image_url(
                uuid="test",
                image_format="jpg",
                rotation=180,
                version="v1"
            )
            self.assertEqual(
                image_url_custom_answer,
                image_url_custom
            )
            self.assertRaises(
                NotFound,
                iiif_image_url,
                size="200,"
            )
