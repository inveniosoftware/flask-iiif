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

from datetime import datetime

from cachelib.redis import RedisCache
from flask import current_app
from redis import StrictRedis

from .cache import ImageCache


class ImageRedisCache(ImageCache):
    """Redis image cache."""

    def __init__(self, app=None):
        """Initialize the cache."""
        super(ImageRedisCache, self).__init__(app=app)
        app = app or current_app
        redis_url = app.config["IIIF_CACHE_REDIS_URL"]
        prefix = app.config.get("IIIF_CACHE_REDIS_PREFIX", "iiif")
        self.cache = RedisCache(host=StrictRedis.from_url(redis_url), key_prefix=prefix)

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
        timeout = timeout or self.timeout
        self.cache.set(key, value, timeout=timeout)
        self.set_last_modification(key, timeout=timeout)

    def get_last_modification(self, key):
        """Get last modification of cached file.

        :param key: the file object's key
        """
        return self.get(self._last_modification_key_name(key))

    def set_last_modification(self, key, last_modification=None, timeout=None):
        """Set last modification of cached file.

        :param key: the file object's key
        :param last_modification: Last modification date of
            file represented by the key
        :type last_modification: datetime.datetime
        :param timeout: the cache timeout in seconds
        """
        if not last_modification:
            last_modification = datetime.utcnow().replace(microsecond=0)
        timeout = timeout or self.timeout
        self.cache.set(
            self._last_modification_key_name(key), last_modification, timeout
        )

    def delete(self, key):
        """Delete the specific key."""
        self.cache.delete(key)
        self.cache.delete(self._last_modification_key_name(key))

    def flush(self):
        """Flush the cache."""
        self.cache.clear()
