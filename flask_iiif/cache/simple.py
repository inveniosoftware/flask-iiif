# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015, 2016, 2017 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Implement a simple cache."""

from __future__ import absolute_import

from werkzeug.contrib.cache import SimpleCache

from .cache import ImageCache


class ImageSimpleCache(ImageCache):
    """Simple image cache."""

    def __init__(self):
        """Initialize the cache."""
        super(ImageSimpleCache, self).__init__()
        self.cache = SimpleCache()

    def get(self, key):
        """Return the key value.

        :param key: the object's key
        :return: the stored object
        :rtype: `BytesIO` object
        """
        return self.cache.get(key)

    def set(self, key, value, timeout=None):
        """Cache the object.

        :param key: the object's key
        :param value: the stored object
        :type value: `BytesIO` object
        :param timeout: the cache timeout in seconds
        """
        timeout = timeout if timeout else self.timeout
        self.cache.set(key, value, timeout)

    def delete(self, key):
        """Delete the specific key."""
        self.cache.delete(key)

    def flush(self):
        """Flush the cache."""
        self.cache.clear()
