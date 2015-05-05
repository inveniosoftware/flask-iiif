# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Image Simple Cache Tests."""

from __future__ import absolute_import

from io import BytesIO

from .helpers import IIIFTestCase


class TestImageSimpleCache(IIIFTestCase):

    """Multimedia Image Simple Cache test case."""

    def setUp(self):
        """Run before the test."""
        # Create a simple cache object
        from PIL import Image
        from flask_iiif.cache.simple import ImageSimpleCache

        # Initialize the cache object
        self.cache = ImageSimpleCache()
        # Create an image in memory
        tmp_file = BytesIO()
        # create a new image
        image = Image.new("RGBA", (1280, 1024), (255, 0, 0, 0))
        image.save(tmp_file, 'png')
        # Store the image
        tmp_file.seek(0)
        self.image_file = tmp_file

    def test_set_and_get_function(self):
        """Test cache set and get functions."""
        # Seek position
        self.image_file.seek(0)
        # Add image to cache
        self.cache.set('image_1', self.image_file.getvalue())
        # Get image from cache
        image_string = self.cache.get('image_1')
        # test if the cache image is equal to the real
        self.assertEqual(image_string, self.image_file.getvalue())

    def test_image_recreation(self):
        """Test the image recreation from cache."""
        from flask_iiif.api import MultimediaImage

        # Seek position
        self.image_file.seek(0)
        # Add the image to cache
        self.cache.set('image_2', self.image_file.getvalue())
        # Get image from cache
        image_string = self.cache.get('image_2')
        # Create a ByteIO object
        cached_image = BytesIO(image_string)
        # Seek object to the right position
        cached_image.seek(0)
        # Create an image object form the stored string
        image = MultimediaImage.from_string(cached_image)
        # Check if the image is still the same
        self.assertEqual(str(image.size()), str((1280, 1024)))

    def test_cache_deletion(self):
        """Test cache delete function."""
        self.cache.set('foo', 'bar')
        self.assertEqual(self.cache.get('foo'), 'bar')
        self.cache.delete('foo')
        self.assertEqual(self.cache.get('foo'), None)

    def test_cache_flush(self):
        """Test cache flush function."""
        self.cache.set('foo_1', 'bar')
        self.cache.set('foo_2', 'bar')
        self.cache.set('foo_3', 'bar')
        for i in [1, 2, 3]:
            self.assertEqual(self.cache.get('foo_{0}'.format(i)), 'bar')
        self.cache.flush()
        for i in [1, 2, 3]:
            self.assertEqual(self.cache.get('foo_{0}'.format(i)), None)
