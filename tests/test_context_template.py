# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2015 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Context Template Tests."""

from .helpers import IIIFTestCase


class TestContextTemplates(IIIFTestCase):

    """Context templates test case."""

    def test_context_tempalte_iiif_image_url(self):
        """Test context template."""
        from werkzeug.exceptions import NotFound
        from flask_iiif.utils import iiif_image_url

        with self.app.app_context():
            image_url_default = iiif_image_url(
                uuid=u"test-ünicode"
            )
            image_url_default_answer = (
                "/api/multimedia/image/v2/"
                "test-%C3%BCnicode/full/full/0/default.png"
            )
            self.assertEqual(
                image_url_default_answer,
                image_url_default
            )
            image_url_custom_answer = (
                "/api/multimedia/image/v1/"
                "test-%C3%BCnicode/full/full/180/default.jpg"
            )
            image_url_custom = iiif_image_url(
                uuid=u"test-ünicode",
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
