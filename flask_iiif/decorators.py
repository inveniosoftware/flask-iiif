# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2015, 2016 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Flask-IIIF decorators."""

from functools import wraps

from flask import current_app
from flask_restful import abort
from werkzeug import LocalProxy

from .errors import IIIFValidatorError, MultimediaError, \
    MultimediaImageCropError, MultimediaImageFormatError, \
    MultimediaImageNotFound, MultimediaImageQualityError, \
    MultimediaImageResizeError, MultimediaImageRotateError

__all__ = ('api_decorator', 'error_handler', )

current_iiif = LocalProxy(lambda: current_app.extensions['iiif'])


def error_handler(f):
    """Error handler."""
    @wraps(f)
    def inner(*args, **kwargs):
        """Wrap the errors."""
        try:
            return f(*args, **kwargs)
        except (MultimediaImageCropError, MultimediaImageResizeError,
                MultimediaImageFormatError, MultimediaImageRotateError,
                MultimediaImageQualityError) as error:
            abort(500, message=error.message, code=500)
        except IIIFValidatorError as error:
            abort(400, message=error.message, code=400)
        except (MultimediaError, MultimediaImageNotFound) as error:
            abort(error.code, message=error.message, code=error.code)
    return inner


def api_decorator(f):
    """Decorate API method."""
    @wraps(f)
    def inner(*args, **kwargs):
        if current_iiif.api_decorator_callback:
            current_iiif.api_decorator_callback(*args, **kwargs)
        return f(*args, **kwargs)
    return inner
