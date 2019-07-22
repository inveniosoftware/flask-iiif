# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2017 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Image Redis Cache Tests."""

from __future__ import absolute_import

from six import BytesIO

from .helpers import IIIFTestCase


class TestImageRedisCache(IIIFTestCase):

    """Multimedia Image Redis Cache test case."""

    def setUp(self):
        """Run before the test."""
        # Create a redis cache object
        from PIL import Image
        from flask_iiif.cache.redis import ImageRedisCache

        # Initialize the cache object
        self.cache = ImageRedisCache()
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

    def test_default_prefix_for_redis(self):
        """Test default redis prefix"""
        # Test default prefix for redis keys (when nothing set in config)
        self.assertEqual(self.cache.cache.key_prefix, 'iiif')

    def test_redis_prefix_set_properly(self):
        """Test if ImageRedisCache properly sets redis prefix"""
        from flask import current_app
        from flask_iiif.cache.redis import ImageRedisCache

        # Store old prefix
        old_prefix = current_app.config.get('IIIF_CACHE_REDIS_PREFIX')
        # Set new prefix in config
        current_app.config['IIIF_CACHE_REDIS_PREFIX'] = "TEST_PREFIX"
        # Create new ImageRedisCache which should read new prefix from config
        tmp_redis_cache = ImageRedisCache()
        # Check prefix set in ImageRedisCache object
        self.assertEqual(tmp_redis_cache.cache.key_prefix, 'TEST_PREFIX')
        # Restore old prefix in config
        current_app.config['IIIF_CACHE_REDIS_PREFIX'] = old_prefix

    def test_removing_keys_removes_only_ones_with_prefix(self):
        """Test if ImageRedisCache properly removes only keys with it's prefix"""
        from flask import current_app
        from flask_iiif.cache.redis import ImageRedisCache

        # Create few keys with default prefix
        self.cache.set('key_1', 'value_1')
        self.cache.set('key_2', 'value_2')
        self.cache.set('key_3', 'value_3')

        # Create RedisCache with different prefix
        old_prefix = current_app.config.get('IIIF_CACHE_REDIS_PREFIX')
        current_app.config['IIIF_CACHE_REDIS_PREFIX'] = "TEST_PREFIX"
        tmp_redis_cache = ImageRedisCache()
        current_app.config['IIIF_CACHE_REDIS_PREFIX'] = old_prefix

        # Create few keys with different prefix
        tmp_redis_cache.set("key_1", "value_4")
        tmp_redis_cache.set("key_2", "value_5")
        tmp_redis_cache.set("key_3", "value_6")

        # Remove all keys with default prefix
        self.cache.flush()

        # Check if keys from second prefix are still in redis
        self.assertEqual(tmp_redis_cache.get("key_1"), "value_4")
        self.assertEqual(tmp_redis_cache.get("key_2"), "value_5")
        self.assertEqual(tmp_redis_cache.get("key_3"), "value_6")
