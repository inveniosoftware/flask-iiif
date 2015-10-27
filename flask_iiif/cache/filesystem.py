# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Implement a filesystem cache."""
import os

from werkzeug.contrib.cache import FileSystemCache

from flask import current_app

from .cache import ImageCache


class ImageFileSystemCache(ImageCache):

    """Filesystem image cache."""

    def __init__(self):
        """Initialize the cache."""
        super(ImageFileSystemCache, self).__init__()
        cache_dir = os.path.join(current_app.config['CFG_TMPDIR'], 'iiif')

        # Create cache folder if not exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        self.cache = FileSystemCache(cache_dir=cache_dir,
                                     threshold=50000,
                                     mode=660)

    def get(self, key):
        """Return the key value.

        :param string key: the object's key
        :return: the stored object
        :rtype: `BytesIO` object
        """
        return self.cache.get(key)

    def set(self, key, value, timeout=None):
        """Cache the object.

        :param string key: the object's key
        :param value: the stored object
        :type value: `BytesIO` object
        :param int timeout: the cache timeout in seconds
        """
        self.cache.set(key, value, timeout)

    def delete(self, key):
        """Delete the specific key."""
        self.cache.delete(key)

    def flush(self):
        """Flush the cache."""
        self.cache.clear()
