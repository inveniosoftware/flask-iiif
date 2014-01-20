# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Multimedia utilities."""

import redis


def initialize_redis():
    """Initialize redis service.

    .. note::

        FIXME: Should be remove it and replaced with an invenio redis object.

    """
    from flask import current_app

    _redis_server = redis.Redis.from_url(
        current_app.config.get('CACHE_REDIS_URL', 'redis://localhost:6379')
    )
    return _redis_server
