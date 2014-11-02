# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Multimedia Image API Tests."""

from io import BytesIO

from .helpers import FlaskTestCase


class TestMultimediaAPI(FlaskTestCase):

    """Multimedia Image API test case."""

    def setUp(self):
        """Run before the test."""
        # Create an image in memory
        from PIL import Image
        from flask_iiif.api import MultimediaImage
        tmp_file = BytesIO()
        # create a new image
        image = Image.new("RGBA", (1280, 1024), (255, 0, 0, 0))
        image.save(tmp_file, 'png')

        # Initialize it for our object and create and instance for
        # each test
        tmp_file.seek(0)
        self.image_resize = MultimediaImage.from_string(tmp_file)
        tmp_file.seek(0)
        self.image_crop = MultimediaImage.from_string(tmp_file)
        tmp_file.seek(0)
        self.image_rotate = MultimediaImage.from_string(tmp_file)

    def test_image_resize(self):
        """Test image resize function."""
        # Test image size before
        self.assertEqual(str(self.image_resize.size()), str((1280, 1024)))

        # Resize.image_resize to 720,680
        self.image_resize.resize('720,680')
        self.assertEqual(str(self.image_resize.size()), str((720, 680)))

        # Resize.image_resize to 300,
        self.image_resize.resize('300,')
        self.assertEqual(str(self.image_resize.size()), str((300, 283)))

        # Resize.image_resize to ,300
        self.image_resize.resize(',300')
        self.assertEqual(str(self.image_resize.size()), str((318, 300)))

        # Resize.image_resize to pct:90
        self.image_resize.resize('pct:90')
        self.assertEqual(str(self.image_resize.size()), str((286, 270)))

    def test_image_crop(self):
        """Test the crop function."""
        # Crop image x,y,w,h
        self.image_crop.crop('20,20,400,300')
        self.assertEqual(str(self.image_crop.size()), str((400, 300)))

        # Crop image pct:x,y,w,h
        self.image_crop.crop('pct:20,20,40,30')
        self.assertEqual(str(self.image_crop.size()), str((160, 90)))

    def test_image_rotate(self):
        """Test image rotate function."""
        self.image_rotate.rotate(90)
        self.assertEqual(str(self.image_rotate.size()), str((1024, 1280)))
