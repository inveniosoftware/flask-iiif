# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2015-2024 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Test REST API."""

from io import BytesIO
from unittest.mock import patch

from flask import url_for
from PIL import Image
from werkzeug.utils import secure_filename

from .helpers import IIIFTestCaseWithRedis


class TestRestAPI(IIIFTestCaseWithRedis):
    """Test signals and decorators."""

    def test_api_base(self):
        """Test API Base."""
        data = dict(uuid="valid:id", version="v2")
        get_the_response = self.get("iiifimagebase", urlargs=data)
        self.assertEqual(get_the_response.status_code, 303)

    def test_api_info(self):
        """Test API Info not found case."""
        from flask import jsonify

        id_v1 = url_for(
            "iiifimagebase", uuid="valid:id-üni", version="v1", _external=True
        )
        id_v2 = url_for(
            "iiifimagebase", uuid="valid:id-üni", version="v2", _external=True
        )

        expected = {
            "v1": {
                "@context": (
                    "http://library.stanford.edu/iiif/" "image-api/1.1/context.json"
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
                "scale_factors": [1, 2, 4, 8, 16, 32, 64],
            },
            "v2": {
                "@context": "http://iiif.io/api/image/2/context.json",
                "@id": id_v2,
                "protocol": "http://iiif.io/api/image",
                "width": 1280,
                "height": 1024,
                "tiles": [{"width": 256, "scaleFactors": [1, 2, 4, 8, 16, 32, 64]}],
                "profile": ["http://iiif.io/api/image/2/level2.json"],
            },
        }
        get_the_response = self.get(
            "iiifimageinfo",
            urlargs=dict(
                uuid="valid:id-üni",
                version="v2",
            ),
        )
        self.assert200(get_the_response)
        get_the_response = self.get(
            "iiifimageinfo",
            urlargs=dict(
                uuid="valid:id-üni",
                version="v2",
            ),
        )
        self.assertEqual(jsonify(expected.get("v2")).data, get_the_response.data)

        get_the_response = self.get(
            "iiifimageinfo",
            urlargs=dict(
                uuid="valid:id-üni",
                version="v1",
            ),
        )
        self.assert200(get_the_response)
        self.assertEqual(jsonify(expected.get("v1")).data, get_the_response.data)

    def test_api_info_not_found(self):
        """Test API Info."""
        get_the_response = self.get(
            "iiifimageinfo",
            urlargs=dict(
                uuid="notfound",
                version="v2",
            ),
        )
        self.assert404(get_the_response)

    def test_api_not_found(self):
        """Test API not found case."""
        get_the_response = self.get(
            "iiifimageapi",
            urlargs=dict(
                uuid="notfound",
                version="v2",
                region="full",
                size="full",
                rotation="0",
                quality="default",
                image_format="png",
            ),
        )
        self.assert404(get_the_response)

    def test_api_internal_server_error(self):
        """Test API internal server error case."""
        get_the_response = self.get(
            "iiifimageapi",
            urlargs=dict(
                uuid="valid:id-üni",
                version="v2",
                region="full",
                size="full",
                rotation="2220",
                quality="default",
                image_format="png",
            ),
        )
        self.assert500(get_the_response)

    def test_api_iiif_validation_error(self):
        """Test API iiif validation case."""
        get_the_response = self.get(
            "iiifimageapi",
            urlargs=dict(
                uuid="valid:id-üni",
                version="v1",
                region="200",
                size="full",
                rotation="2220",
                quality="default",
                image_format="png",
            ),
        )
        self.assert400(get_the_response)

    def test_api_stream_image(self):
        """Test API stream image."""
        tmp_file = BytesIO()
        # create a new image
        image = Image.new("RGBA", (1280, 1024), (255, 0, 0, 0))
        image.save(tmp_file, "png")
        tmp_file.seek(0)
        get_the_response = self.get(
            "iiifimageapi",
            urlargs=dict(
                uuid="valid:id-üni",
                version="v2",
                region="full",
                size="full",
                rotation="0",
                quality="default",
                image_format="png",
            ),
        )
        # Check if returns `Last-Modified` key in headers
        # required for `If-Modified-Since`
        self.assertTrue("Last-Modified" in get_the_response.headers)

        last_modified = get_the_response.headers["Last-Modified"]

        self.assertEqual(get_the_response.data, tmp_file.getvalue())

        # Test `If-Modified-Since` recognized properly
        get_the_response = self.get(
            "iiifimageapi",
            urlargs=dict(
                uuid="valid:id-üni",
                version="v2",
                region="full",
                size="full",
                rotation="0",
                quality="default",
                image_format="png",
            ),
            headers={"If-Modified-Since": last_modified},
        )

        self.assertEqual(get_the_response.status_code, 304)

        urlargs = dict(
            uuid="valid:id-üni",
            version="v2",
            region="200,200,200,200",
            size="300,300",
            rotation="!50",
            quality="color",
            image_format="pdf",
        )

        get_the_response = self.get(
            "iiifimageapi",
            urlargs=urlargs,
        )
        self.assert200(get_the_response)

        default_name = "{name}-200200200200-300300-color-50.pdf".format(
            name=secure_filename(urlargs["uuid"])
        )
        for dl, name in (
            ("", default_name),
            ("1", default_name),
            ("foo.pdf", "foo.pdf"),
        ):
            urlargs["dl"] = dl
            get_the_response = self.get(
                "iiifimageapi",
                urlargs=urlargs,
            )
            self.assert200(get_the_response)
            self.assertEqual(
                get_the_response.headers["Content-Disposition"],
                "attachment; filename={name}".format(name=name),
            )

    def test_api_decorator(self):
        """Test API decorator."""
        get_the_response = self.get(
            "iiifimageapi",
            urlargs=dict(
                uuid="valid:decorator:id",
                version="v2",
                region="full",
                size="full",
                rotation="0",
                quality="default",
                image_format="png",
            ),
        )
        self.assert403(get_the_response)

    def test_api_abort_all_methods_except_get(self):
        """Abort all methods but GET."""
        data = dict(
            uuid="valid:id-üni",
            version="v2",
            region="full",
            size="full",
            rotation="0",
            quality="default",
            image_format="png",
        )
        get_the_response = self.post("iiifimageapi", urlargs=data)
        self.assert405(get_the_response)

        get_the_response = self.put("iiifimageapi", urlargs=data)
        self.assert405(get_the_response)

        get_the_response = self.delete("iiifimageapi", urlargs=data)
        self.assert405(get_the_response)

        get_the_response = self.patch("iiifimageapi", urlargs=data)
        self.assert405(get_the_response)

    def test_api_cache_control(self):
        """Test cache-control headers"""

        urlargs = dict(
            uuid="valid:id-üni",
            version="v2",
            region="200,200,200,200",
            size="300,300",
            rotation="!50",
            quality="color",
            image_format="pdf",
        )

        key = "iiif:{0}/{1}/{2}/{3}/{4}.{5}".format(
            urlargs["uuid"],
            urlargs["region"],
            urlargs["size"],
            urlargs["quality"],
            urlargs["rotation"],
            urlargs["image_format"],
        )

        cache = self.app.config["IIIF_CACHE_HANDLER"].cache

        get_the_response = self.get(
            "iiifimageapi",
            urlargs=urlargs,
        )

        self.assertFalse("cache-control" in urlargs)

        self.assert200(get_the_response)

        self.assertTrue(cache.get(key))

        cache.clear()

        for cache_control, name in (("no-cache", "foo.pdf"), ("no-store", "foo.pdf")):
            urlargs["cache-control"] = cache_control

            get_the_response = self.get(
                "iiifimageapi",
                urlargs=urlargs,
            )

            self.assert200(get_the_response)

            self.assertFalse(cache.get(key))

            cache.clear()

        for cache_control, name in (("public", "foo.pdf"), ("no-transform", "foo.pdf")):
            urlargs["cache-control"] = cache_control

            get_the_response = self.get(
                "iiifimageapi",
                urlargs=urlargs,
            )

            self.assert200(get_the_response)

            self.assertTrue(cache.get(key))

            cache.clear()

    def test_cache_ignore_errors(self):
        """Test if cache retrieval errors are ignored when configured."""
        from flask import current_app

        info_args = dict(uuid="valid:id", version="v2")
        api_args = dict(
            uuid="valid:id",
            version="v2",
            region="full",
            size="full",
            rotation="0",
            quality="default",
            image_format="png",
        )

        cache = self.app.config["IIIF_CACHE_HANDLER"].cache
        with patch.object(cache, "get", side_effect=Exception("test fail")):
            # Without ignoring errors
            self.assertRaisesRegex(
                Exception, "test fail", self.get, "iiifimageinfo", urlargs=info_args
            )
            self.assertRaisesRegex(
                Exception, "test fail", self.get, "iiifimageapi", urlargs=api_args
            )

            # Ignore errors
            old_value = current_app.config.get("IIIF_CACHE_IGNORE_ERRORS")
            current_app.config["IIIF_CACHE_IGNORE_ERRORS"] = True

            resp = self.get("iiifimageinfo", urlargs=info_args)
            self.assert200(resp)
            resp = self.get("iiifimageapi", urlargs=api_args)
            self.assert200(resp)

            current_app.config["IIIF_CACHE_REDIS_PREFIX"] = old_value
