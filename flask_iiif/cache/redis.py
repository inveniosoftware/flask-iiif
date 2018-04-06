# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2016, 2017 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Implements a Redis cache."""

from __future__ import absolute_import

from flask import current_app
from redis import StrictRedis
from werkzeug.contrib.cache import RedisCache

from .cache import ImageCache


class ImageRedisCache(ImageCache):
    """Redis image cache."""

    def __init__(self):
        """Initialize the cache."""
        super(ImageRedisCache, self).__init__()
        redis_url = current_app.config['IIIF_CACHE_REDIS_URL']
        self.cache = RedisCache(host=StrictRedis.from_url(redis_url))

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
        self.cache.set(key, value, timeout=timeout)

    def delete(self, key):
        """Delete the specific key."""
        self.cache.delete(key)

    def flush(self):
        """Flush the cache."""
        self.cache.clear()
