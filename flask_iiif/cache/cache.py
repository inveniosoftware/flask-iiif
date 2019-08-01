# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015, 2017 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Abstract simple cache definition.

All cache adaptors must at least implement
:func:`~flask_iiif.cache.cache.ImageCache.get` and
:func:`~flask_iiif.cache.cache.ImageCache.set` methods.
"""

from flask import current_app
from werkzeug import cached_property


class ImageCache(object):
    """Abstract cache layer."""

    def __init__(self):
        """Initialize the cache."""

    @cached_property
    def timeout(self):
        """Return default timeout from config."""
        return current_app.config['IIIF_CACHE_TIME']

    def get(self, key):
        """Return the key value.

        :param key: the object's key
        """

    def set(self, key, value, timeout=None):
        """Cache the object.

        :param key: the object's key
        :param value: the stored object
        :type value: :class:`StringIO.StringIO` object
        :param timeout: the cache timeout in seconds
        """

    def get_last_modification(self, key):
        """Get last modification of cached file.

        :param key: the file object's key
        """

    def set_last_modification(self, key, last_modification=None, timeout=None):
        """Set last modification of cached file.

        :param key: the file object's key
        :param last_modification: Last modification date of
            file represented by the key
        :type last_modification: datetime
        :param timeout: the cache timeout in seconds
        """

    def _last_modification_key_name(self, key):
        """Generate key for last_modification entry of specified key.

        :param key: the file object's key
        """
        return "last_modification::%s" % key

    def delete(self, key):
        """Delete the specific key."""

    def flush(self):
        """Flush the cache."""
