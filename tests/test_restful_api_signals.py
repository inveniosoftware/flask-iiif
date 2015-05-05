# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2015 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Test REST API signals."""

from .helpers import IIIFTestCase, signal_listener


class TestRestAPISignals(IIIFTestCase):

    """Test REST API signals."""

    def test_api_signals(self):
        """Test API signals."""
        from flask_iiif.signals import (
            iiif_after_process_request, iiif_before_process_request
        )

        data = dict(
            uuid='valid:id',
            version='v2',
            region='full',
            size='full',
            rotation='0',
            quality='default',
            image_format='png'
        )

        with signal_listener(iiif_before_process_request) as listener:
            self.get(
                'iiifimageapi',
                urlargs=data
            )
            results = listener.assert_signal()
            self.assertEqual(
                results[1],
                data
            )

        with signal_listener(iiif_after_process_request) as listener:
            response = self.get(
                'iiifimageapi',
                urlargs=data
            )
            results = listener.assert_signal()
            self.assertEqual(
                (results[1].get('mimetype'),
                 results[1].get('image').getvalue()),
                ('image/png', response.data)
            )
