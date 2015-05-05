# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2015 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Test REST API."""

from io import BytesIO

from PIL import Image

from .helpers import IIIFTestCase


class TestRestAPI(IIIFTestCase):

    """Test signals and decorators."""

    def test_api_not_found(self):
        """Test API not found case."""
        get_the_response = self.get(
            'iiifimageapi',
            urlargs=dict(
                uuid='notfound',
                version='v2',
                region='full',
                size='full',
                rotation='0',
                quality='default',
                image_format='png'
            )
        )
        self.assert404(get_the_response)

    def test_api_internal_server_error(self):
        """Test API internal server error case."""
        get_the_response = self.get(
            'iiifimageapi',
            urlargs=dict(
                uuid='valid:id',
                version='v2',
                region='full',
                size='full',
                rotation='2220',
                quality='default',
                image_format='png'
            )
        )
        self.assert500(get_the_response)

    def test_api_iiif_validation_error(self):
        """Test API iiif validation case."""
        get_the_response = self.get(
            'iiifimageapi',
            urlargs=dict(
                uuid='valid:id',
                version='v1',
                region='200',
                size='full',
                rotation='2220',
                quality='default',
                image_format='png'
            )
        )
        self.assert400(get_the_response)

    def test_api_stream_image(self):
        """Test API stream image."""
        tmp_file = BytesIO()
        # create a new image
        image = Image.new("RGBA", (1280, 1024), (255, 0, 0, 0))
        image.save(tmp_file, 'png')
        tmp_file.seek(0)

        get_the_response = self.get(
            'iiifimageapi',
            urlargs=dict(
                uuid='valid:id',
                version='v2',
                region='full',
                size='full',
                rotation='0',
                quality='default',
                image_format='png'
            )
        )

        self.assertEqual(
            get_the_response.data,
            tmp_file.getvalue()
        )

        get_the_response = self.get(
            'iiifimageapi',
            urlargs=dict(
                uuid='valid:id',
                version='v2',
                region='200,200,200,200',
                size='300,300',
                rotation='!50',
                quality='color',
                image_format='pdf'
            )
        )
        self.assert200(get_the_response)

    def test_api_decorator(self):
        """Test API decorator."""
        get_the_response = self.get(
            'iiifimageapi',
            urlargs=dict(
                uuid='valid:decorator:id',
                version='v2',
                region='full',
                size='full',
                rotation='0',
                quality='default',
                image_format='png'
            )
        )
        self.assert403(get_the_response)
