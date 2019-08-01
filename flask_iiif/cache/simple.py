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

from datetime import datetime

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
        self.set_last_modification(key, timeout=timeout)

    def get_last_modification(self, key):
        """Get last modification of cached file.

        :param key: the file object's key
        """
        last = self.cache.get(self._last_modification_key_name(key))
        return last

    def set_last_modification(self, key, last_modification=None, timeout=None):
        """Set last modification of cached file.

        :param key: the file object's key
        :param last_modification: Last modification date of
            file represented by the key
        :type last_modification: datetime
        :param timeout: the cache timeout in seconds
        """
        if not key:
            return
        if not last_modification:
            last_modification = datetime.utcnow().replace(microsecond=0)
        timeout = timeout if timeout else self.timeout
        self.cache.set(
            self._last_modification_key_name(key),
            last_modification,
            timeout
        )

    def delete(self, key):
        """Delete the specific key."""
        if key:
            self.cache.delete(key)
            self.cache.delete(self._last_modification_key_name(key))

    def flush(self):
        """Flush the cache."""
        self.cache.clear()
