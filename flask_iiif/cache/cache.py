# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Abstract simple cache definition.

All cache adaptors must at least implement
:func:`~flask_iiif.cache.cache.ImageCache.get` and
:func:`~flask_iiif.cache.cache.ImageCache.set` methods.
"""


class ImageCache(object):

    """Abstract cache layer."""

    timeout = 60 * 60 * 24 * 2

    def __init__(self):
        """Initialize the cache."""

    def get(self, key):
        """Return the key value.

        :param string key: The object's key
        """

    def set(self, key, value, timeout=timeout):
        """Cache the object.

        :param string key: The object's key
        :param value: the stored object
        :type value: :class:`StringIO.StringIO` object
        :param int timeout: The cache timeout in seconds
        """

    def delete(self, key):
        """Delete the specific key."""

    def flush(self):
        """Flush the cache."""
