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

from flask import url_for
from PIL import Image
from werkzeug.utils import secure_filename

from .helpers import IIIFTestCase


class TestRestAPI(IIIFTestCase):

    """Test signals and decorators."""

    def test_api_base(self):
        """Test API Base."""
        data = dict(
            uuid="valid:id",
            version="v2"
        )
        get_the_response = self.get(
            'iiifimagebase',
            urlargs=data
        )
        self.assertEqual(get_the_response.status_code, 303)

    def test_api_info(self):
        """Test API Info not found case."""
        from flask import jsonify
        id_v1 = url_for(
            'iiifimagebase', uuid=u"valid:id-üni", version="v1", _external=True
        )
        id_v2 = url_for(
            'iiifimagebase', uuid=u"valid:id-üni", version="v2", _external=True
        )

        expected = {
            "v1": {
                "@context": (
                    "http://library.stanford.edu/iiif/"
                    "image-api/1.1/context.json"
                ),
                "@id": id_v1,
                "width": 1280,
                "height": 1024,
                "profile": (
                    "http://library.stanford.edu/iiif/image-api/compliance"
                    ".html#level1"
                ),
                "tile_width": 256,
                "tile_height": 256,
                "scale_factors": [
                    1, 2, 4, 8, 16, 32, 64
                ]
            },
            "v2": {
                "@context": "http://iiif.io/api/image/2/context.json",
                "@id": id_v2,
                "protocol": "http://iiif.io/api/image",
                "width": 1280,
                "height": 1024,
                "tiles": [
                    {
                        "width": 256,
                        "scaleFactors": [
                            1, 2, 4, 8, 16, 32, 64
                        ]
                    }
                ],
                "profile": [
                    "http://iiif.io/api/image/2/level2.json",
                ]
            }
        }
        get_the_response = self.get(
            'iiifimageinfo',
            urlargs=dict(
                uuid=u'valid:id-üni',
                version='v2',
            )
        )
        self.assert200(get_the_response)
        get_the_response = self.get(
            'iiifimageinfo',
            urlargs=dict(
                uuid=u'valid:id-üni',
                version='v2',
            )
        )
        self.assertEqual(
            jsonify(expected.get('v2')).data, get_the_response.data
        )

        get_the_response = self.get(
            'iiifimageinfo',
            urlargs=dict(
                uuid=u'valid:id-üni',
                version='v1',
            )
        )
        self.assert200(get_the_response)
        self.assertEqual(
            jsonify(expected.get('v1')).data, get_the_response.data
        )

    def test_api_info_not_found(self):
        """Test API Info."""
        get_the_response = self.get(
            'iiifimageinfo',
            urlargs=dict(
                uuid='notfound',
                version='v2',
            )
        )
        self.assert404(get_the_response)

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
                uuid=u'valid:id-üni',
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
                uuid='valid:id-üni',
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
                uuid=u'valid:id-üni',
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

        urlargs = dict(
            uuid=u'valid:id-üni',
            version='v2',
            region='200,200,200,200',
            size='300,300',
            rotation='!50',
            quality='color',
            image_format='pdf',
        )

        get_the_response = self.get(
            'iiifimageapi',
            urlargs=urlargs,
        )
        self.assert200(get_the_response)

        default_name = u'{name}-200200200200-300300-color-50.pdf'.format(
            name=secure_filename(urlargs['uuid'])
        )
        for dl, name in (('', default_name), ('1', default_name),
                         ('foo.pdf', 'foo.pdf')):
            urlargs['dl'] = dl
            get_the_response = self.get(
                'iiifimageapi',
                urlargs=urlargs,
            )
            self.assert200(get_the_response)
            self.assertEqual(
                get_the_response.headers['Content-Disposition'],
                'attachment; filename={name}'.format(name=name)
            )

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

    def test_api_abort_all_methods_except_get(self):
        """Abort all methods but GET."""
        data = dict(
            uuid='valid:id-üni',
            version='v2',
            region='full',
            size='full',
            rotation='0',
            quality='default',
            image_format='png'
        )
        get_the_response = self.post(
            'iiifimageapi',
            urlargs=data
        )
        self.assert405(get_the_response)

        get_the_response = self.put(
            'iiifimageapi',
            urlargs=data
        )
        self.assert405(get_the_response)

        get_the_response = self.delete(
            'iiifimageapi',
            urlargs=data
        )
        self.assert405(get_the_response)

        get_the_response = self.patch(
            'iiifimageapi',
            urlargs=data
        )
        self.assert405(get_the_response)
